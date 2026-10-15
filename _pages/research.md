---
title: "Research"
permalink: /research/
layout: single
author_profile: true
classes: wide
header:
  image: /assets/images/Qwen_image_2.1_00018.png
  image_description: An AI-generated image depicting an intense probe pulse breaking the pumped molecule into fragments.
  caption: An AI-generated image depicting an intense probe pulse breaking the pumped molecule into fragments. Created by Qwen-Image-2.1 on ComfyUI.
gallery:
  - image_path: /assets/images/before_tunneling.svg
    alt: "Before tunneling ionization"
  - image_path: /assets/images/during_tunneling.svg
    alt: "During tunneling ionization"
  - image_path: /assets/images/after_tunneling.svg
    alt: "After tunneling ionization"
gallery_buildup:
  - image_path: /assets/images/two-level.png
    alt: "Effective two-level system of the nitrogen molecular ion"
  - image_path: /assets/images/coh-amp.png
    alt: "Coherence amplitude as a function of laser intensity and wavelength"
  - image_path: /assets/images/buildup-phase.png
    alt: "Subcycle buildup of the electronic coherence at 1341 nm and 1644 nm"
---

Electrons move through molecules on attosecond-to-femtosecond timescales, driving the flow of charge and energy that governs chemical and quantum phenomena. Understanding and controlling the electronic coherence behind this motion is essential for directing charge migration, steering photochemical reactions, and harnessing quantum effects. My research develops theoretical tools to diagnose and control electronic coherence, opening new pathways toward controlling quantum dynamics in molecules. 

## Creating electronic coherence in molecules

{% include gallery class="tunneling-sequence" caption="Schematic of the multielectron tunneling ionization process: before, during, and after tunneling." %}

- Before the laser field arrives, all electrons are bound under the Coulomb potential. Suppose the active electron (solid purple circle) will be ionized.

- The laser field arrives and bends the Coulomb potential, and the active electron tunnels out. The remaining electrons are frozen.

- After tunneling, the ionized electron is mainly driven by the laser, while the laser can excite the hole state.

- An electron in red circles can undergo the same process, forming a different hole state. 

- Multielectron tunneling ionization thus creates a superposition of ionic states and their electronic coherence.

Reference: 
1. C.H. Yuen, Nonadiabatic theory for subcycle ionic dynamics in multielectron tunneling ionization, Physical Review A 113 (4), 043125 (2026)

## Example of a nitrogen molecule

<div class="media-cluster align-right">
  <figure>
    <video autoplay loop muted playsinline preload="metadata" class="synced-media">
      <source src="{{ '/assets/images/N2p.mp4' | relative_url }}" type="video/mp4">
    </video>
    <figcaption>Nuclear dynamics of N<sub>2</sub><sup>+</sup>. The vertical line indicates the equilibrium distance of N<sub>2</sub>.</figcaption>
  </figure>
  <figure>
    <video autoplay loop muted playsinline preload="metadata" class="synced-media">
      <source src="{{ '/assets/images/45_hole_dyn.mp4' | relative_url }}" type="video/mp4">
    </video>
    <figcaption>Electron dynamics in N<sub>2</sub><sup>+</sup> molecule initiated by an intense few-cycle infrared laser.</figcaption>
  </figure>
</div>
<script>
(function () {
  function syncVideos() {
    var vids = document.querySelectorAll('video.synced-media');
    if (vids.length < 2) return;
    var a = vids[0], b = vids[1];
    var tolerance = 0.2;

    function resetTogether() {
      if (Math.abs(a.currentTime - b.currentTime) > tolerance) {
        a.currentTime = 0;
        b.currentTime = 0;
      }
    }

    function resync() {
      if (!a.paused && !b.paused &&
          Math.abs(a.currentTime - b.currentTime) > tolerance) {
        b.currentTime = a.currentTime;
      }
    }

    function tryPlay() {
      if (a.readyState >= 2 && b.readyState >= 2) {
        resetTogether();
        a.play().catch(function () {});
        b.play().catch(function () {});
      }
    }

    [a, b].forEach(function (v) {
      v.addEventListener('canplay', tryPlay);
      v.addEventListener('seeked', resync);
      v.addEventListener('playing', resync);
      v.addEventListener('timeupdate', resync);
    });

    // Ensure both start from the same point on initial page load
    window.addEventListener('load', resetTogether);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', syncVideos);
  } else {
    syncVideos();
  }
})();
</script>

- When an N<sub>2</sub> molecule is tunnel ionized by an intense few-cycle infrared pulse, it can form the <em>X</em><sup>2</sup>Σ<sub>g</sub><sup>+</sup> (red curve), <em>A</em><sup>2</sup>Π<sub>u</sub> (blue curve), and <em>B</em><sup>2</sup>Σ<sub>u</sub><sup>+</sup> (green curve) states of N<sub>2</sub><sup>+</sup>.

- The nuclear wave packet moves around the minimum of the potential after the end of the pulse at <em>t</em> = 12 fs.

- Differences in the nuclear motion of the respective states lead to a varying electronic coherence that is proportional to the nuclear overlap.

- After around <em>t</em> = 20 fs, the nuclear wave packet of the <em>A</em><sup>2</sup>Π<sub>u</sub> state has little overlap with the other two states, so that the electron motion pauses.

- As nuclear wave packets overlap well at a later time, the electron motion resumes.

- **This kind of dynamics occurs for other diatomic molecules after ionization. But for polyatomic molecules, some nuclear wave packets may not return close to the equilibrium position due to extra degrees of freedom. Can we find long-lived electronic coherence in polyatomic molecules?**

References: 
1. C.H. Yuen, Nonadiabatic theory for subcycle ionic dynamics in multielectron tunneling ionization, Physical Review A 113 (4), 043125 (2026)
2. C.H. Yuen and C.D. Lin, Coherence from multiorbital tunneling ionization of molecules, Physical Review A 108 (2), 023123 (2023)

## Controlling the electronic coherence

{% include gallery id="gallery_buildup" class="tunneling-sequence" caption="Left: An effective two-level system formed by the <em>X</em><sup>2</sup>Σ<sub>g</sub><sup>+</sup> and <em>B</em><sup>2</sup>Σ<sub>u</sub><sup>+</sup> states of N<sub>2</sub><sup>+</sup>. Middle: Coherence amplitude as a function of laser intensity and wavelength, where the red dashed lines mark the constructive-buildup condition. Right: Subcycle buildup of the electronic coherence at 1341 nm and 1644 nm." %}

- When the N<sub>2</sub> molecule is aligned with the laser polarization, tunnel ionization followed by excitation predominantly populates the <em>X</em><sup>2</sup>Σ<sub>g</sub><sup>+</sup> and <em>B</em><sup>2</sup>Σ<sub>u</sub><sup>+</sup> states of N<sub>2</sub><sup>+</sup>, which together form an effective two-level system.

- The electronic coherence created by multielectron tunneling at different times interferes, so that it either builds up or cancels out. Can we control the timing of this interference to amplify the coherence?

- When the laser frequency is much smaller than the energy separation between the <em>X</em><sup>2</sup>Σ<sub>g</sub><sup>+</sup> and <em>B</em><sup>2</sup>Σ<sub>u</sub><sup>+</sup> states, strong-field excitation enters the **adiabatic** regime.

- In this regime, the conditions for constructive and destructive buildup are given approximately by <em>E</em><sub>XB</sub> + <em>α</em> = (2<em>n</em> + 1)<em>ω</em> and <em>E</em><sub>XB</sub> + <em>α</em> = 2<em>nω</em>, respectively, where <em>E</em><sub>XB</sub> is the energy separation between the two states, <em>α</em> is the AC Stark shift, and <em>n</em> is an integer.

- As an example, when the peak laser intensity is 2.0 × 10<sup>14</sup> W/cm<sup>2</sup>, the coherence builds up constructively every half optical cycle for a 1644 nm laser, whereas it interferes destructively for a 1341 nm laser. Their final coherence amplitudes differ by five orders of magnitude.

- **Can this control scheme be extended to other molecules?**

Reference:
1. C.H. Yuen, Enhanced excited-state population and coherence via adiabatic tunneling ionization and excitation, Physical Review A 113 (1), 013125 (2026)

## Probing electronic coherence in molecules

<div class="media-cluster align-right">
  <figure>
    <img src="{{ '/assets/images/ATAS.png' | relative_url }}" alt="Attosecond transient absorption spectrogram of the nitrogen molecular ion">
    <figcaption>Attosecond transient absorption spectrogram of N<sub>2</sub><sup>+</sup> as a function of the pump-probe delay.</figcaption>
  </figure>
  <figure>
    <img src="{{ '/assets/images/KER_t.png' | relative_url }}" alt="Kinetic energy release spectrum of the ionic fragments as a function of time delay">
    <figcaption>Kinetic energy release (KER) spectrum of the ionic fragments from strong-field dissociative sequential double ionization as a function of the pump-probe delay.</figcaption>
  </figure>
</div>

- We start electron motion with one laser pulse, wait for a controlled time, and then take a "snapshot" with a second pulse. By combining snapshots taken at many different times, we create a movie of how electrons move inside a molecule.

- One way to probe the electron motion is attosecond transient absorption spectroscopy (ATAS). An isolated attosecond pulse interacts with the molecular ion at a chosen delay after the pump pulse. The electronic coherence leaves characteristic fingerprints on the absorption spectrum of the attosecond pulse, allowing us to track how the electronic wave packet evolves in time.

- In the example of N<sub>2</sub><sup>+</sup>, only the coherence between the <em>A</em><sup>2</sup>Π<sub>u</sub> and <em>B</em><sup>2</sup>Σ<sub>u</sub><sup>+</sup> states is imprinted in the absorption band at 391 eV.

- Another approach is called strong-field dissociative sequential double ionization (DSDI). It uses an intense infrared laser pulse arriving after the pump pulse. This pulse first drives transitions between ionic electronic states, making the response sensitive to the amplitude of electronic coherence. It then removes a second electron from the excited states, creating a doubly charged molecular ion that breaks apart. By measuring the resulting ionic fragments, we obtain information about the underlying electron motion.

- The oscillation in the kinetic energy release of N<sup>+</sup> + N<sup>+</sup> at different delays contains information about the all three pairs of electronic coherence.

- Both approaches have important limitations. ATAS captures only part of the electronic motion, while DSDI provides access to a more complete picture but strongly perturbs the molecular ion during the measurement process. As a result, neither technique directly reveals the unperturbed electron dynamics. **Can we design a probe that is both highly informative and minimally invasive?**

References:

1. C.H. Yuen and C.D. Lin, Probing vibronic coherence in charge migration in molecules using strong-field sequential double ionization, Physical Review A 109 (1), L011101 (2024)

2. C.H. Yuen and C.D. Lin, Theory of strong-field sequential double ionization of polyatomic molecules, Physical Review A 109 (3), 033108 (2024)

3. C.H. Yuen and C.D. Lin, Rotation in attosecond vibronic coherence spectroscopy for molecules, Communications Physics 7 (1) (2024)

4. E. Weckwerth, A.J. Howard, C. Cheng, I. Gabalski, A.M. Ghrist, S.A. Mohideen, C.D. Lin, C.H. Yuen and P.H. Bucksbaum, Optical interference effect in strong-field electronic coherence spectroscopy, Physical Review A 112 (4), 043113 (2025)