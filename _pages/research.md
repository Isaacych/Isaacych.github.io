---
title: "Research"
permalink: /research/
layout: single
author_profile: true
classes: wide
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
  - image_path: /assets/images/buildup-phase.png
    alt: "Subcycle buildup of the electronic coherence at 1341 nm and 1644 nm"
  - image_path: /assets/images/coh-amp.png
    alt: "Coherence amplitude as a function of laser intensity and wavelength"
---

Electrons move through molecules on attosecond-to-femtosecond timescales, driving the flow of charge and energy that governs chemical and quantum phenomena. Understanding and controlling the electronic coherence behind this motion is essential for directing charge migration, steering photochemical reactions, and harnessing quantum effects. My research develops theoretical tools to diagnose and control electronic coherence, opening new pathways toward controlling quantum dynamics in molecules. 

## Creating electronic coherence in molecules

{% include gallery class="tunneling-sequence" caption="Schematic of the multielectron tunneling ionization process: before, during, and after tunneling." %}

- Before the laser field arrives, all electrons are bound under the Coulomb potential. Suppose the active electron (solid purple circle) will be ionized.

- The laser field arrives and bends the Coulomb potential, and the active electron is tunneling out. The remaining electrons are frozen.

- After tunneling, the ionized electron is mainly driven by the laser, while the laser can excite the hole state.

- An electron in red circles can undergo the same process, forming a different hole state. 

- Multielectron tunneling ionization thus creates a superposition of ionic states and their electronic coherence.

Reference: 
1. C.H. Yuen, Nonadiabatic theory for subcycle ionic dynamics in multielectron tunneling ionization, Physical Review A 113 (4), 043125 (2026)

## Example of an nitrogen molecule

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

- When an N<sub>2</sub> molecule is tunnel ionized by an intense few-cycle infrared pulse, it could form the <em>X</em><sup>2</sup>Σ<sub>g</sub><sup>+</sup> (red curve), <em>A</em><sup>2</sup>Π<sub>u</sub> (blue curve), and <em>B</em><sup>2</sup>Σ<sub>u</sub><sup>+</sup> (green curve) states of N<sub>2</sub><sup>+</sup>.

- The nuclear wave packet moves around the minimum of the potential after the end of pulse at <em>t</em> = 12 fs.

- Differences in the nuclear motion of the respective states lead to a varying electronic coherence which is proportional to the nuclear overlap.

- After around <em>t</em> = 20 fs, the nuclear wave packet of the <em>A</em><sup>2</sup>Π<sub>u</sub> state has little overlap with the other two states, so that the electron motion pauses.

- As nuclear wave packets overlap well at a later time, the electron motion resumes.

- **This kind of dynamics occurs for other diatomic molecules after ionization. But for polyatomic molecules, some nuclear wave packets may not return close to the equilibrium position due to extra degrees of freedom. Can we find long-lived electronic coherence in polyatomic molecules?**

Reference: 
1. C.H. Yuen, Nonadiabatic theory for subcycle ionic dynamics in multielectron tunneling ionization, Physical Review A 113 (4), 043125 (2026)
2. C.H. Yuen and C.D. Lin, Coherence from multiorbital tunneling ionization of molecules, Physical Review A 108 (2), 023123 (2023)

## Controlling the electronic coherence

{% include gallery id="gallery_buildup" class="tunneling-sequence" caption="Left: An effective two-level system formed by the <em>X</em><sup>2</sup>Σ<sub>g</sub><sup>+</sup> and <em>B</em><sup>2</sup>Σ<sub>u</sub><sup>+</sup> states of N<sub>2</sub><sup>+</sup>. Middle: Buildup of the electronic coherence at 1341 nm and 1644 nm. Right: Coherence amplitude as a function of laser intensity and wavelength, where the red dashed lines mark the constructive-buildup condition." %}

- As mentioned above, multielectron tunneling ionization creates electronic coherence in ionic states. The coherence created at different times would interfere to strengthen or dampen the amplitude. Can we control the timing to amplify it significantly?

- When the N<sub>2</sub> molecule is aligned with the laser polarization, tunnel ionization and excitation predominantly forms the <em>X</em><sup>2</sup>Σ<sub>g</sub><sup>+</sup> and <em>B</em><sup>2</sup>Σ<sub>u</sub><sup>+</sup> states of N<sub>2</sub><sup>+</sup>. As a result, we have an effective two-level system.

- When the laser frequency is much smaller than the energy separation between the <em>X</em><sup>2</sup>Σ<sub>g</sub><sup>+</sup> and <em>B</em><sup>2</sup>Σ<sub>u</sub><sup>+</sup> states, we enter the **adiabatic** regime for strong-field excitation. 

- The condition for constructive coherence buildup follows approximately as <em>E</em><sub>XB</sub> + <em>α</em> = (2<em>n</em> + 1)<em>ω</em>, while the destructive coherence buildup follows <em>E</em><sub>XB</sub> + <em>α</em> = 2<em>nω</em>. Here <em>α</em> is the ac Stark shift between the two states.

Reference:
1. C.H. Yuen, Enhanced excited-state population and coherence via adiabatic tunneling ionization and excitation, Physical Review A 113 (1), 013125 (2026)

## Probing electronic coherence in molecules

- C.H. Yuen and C.D. Lin, Rotation in attosecond vibronic coherence spectroscopy for molecules, Communications Physics 7 (1) (2024)

- C.H. Yuen and C.D. Lin, Theory of strong-field sequential double ionization of polyatomic molecules, Physical Review A 109 (3), 033108 (2024)

- C.H. Yuen and C.D. Lin, Probing vibronic coherence in charge migration in molecules using strong-field sequential double ionization, Physical Review A 109 (1), L011101 (2024)
