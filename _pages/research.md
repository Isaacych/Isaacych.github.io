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
---

Electrons move through molecules on attosecond-to-femtosecond timescales, driving the flow of charge and energy that governs chemical and quantum phenomena. Understanding and controlling the electronic coherence behind this motion is essential for directing charge migration, steering photochemical reactions, and harnessing quantum effects. My research develops theoretical tools to diagnose and control electronic coherence, opening new pathways toward controlling quantum dynamics in molecules. 

## Creating electronic coherence in molecules

{% include gallery class="tunneling-sequence" caption="Schematic of the multielectron tunneling ionization process: before, during, and after tunneling." %}

- Before the laser field arrives, all electrons are bound under the Coulomb potential. Suppose the active electron (solid purple circle) will be ionized.

- The laser field arrives and bends the Coulomb potential, and the active electron is tunneling out. The remaining electrons are frozen.

- After tunneling, the ionized electron is mainly driven by the laser, while the laser could excite the hole state.

- An electron in red circles could undergo the same process, forming a different hole state. 

- Multielectron tunneling ionization thus create a superposition of ionic states and their electronic coherence.

- Reference: C.H. Yuen, Nonadiabatic theory for subcycle ionic dynamics in multielectron tunneling ionization, Physical Review A 113 (4), 043125 (2026)

<div class="media-cluster align-right">
  <figure>
    <video autoplay loop muted playsinline preload="metadata">
      <source src="{{ '/assets/images/N2p.mp4' | relative_url }}" type="video/mp4">
    </video>
    <figcaption>Nuclear dynamics of N<sub>2</sub><sup>+</sup>. Vertical line indicates the equilibrium distance of N<sub>2</sub>.</figcaption>
  </figure>
  <figure>
    <img src="{{ '/assets/images/45_hole_dyn.gif' | relative_url }}" alt="Electron dynamics in N2+ molecule initiated by an intense few-cycle infrared laser">
    <figcaption>Electron dynamics in N<sub>2</sub><sup>+</sup> molecule initiated by an intense few-cycle infrared laser.</figcaption>
  </figure>
</div>

- As an example, when a N<sub>2</sub> molecule is tunnel ionized, it could form the <em>X</em><sup>2</sup>Σ<sub>g</sub><sup>+</sup> (red curve), <em>A</em><sup>2</sup>Π<sub>u</sub> (blue curve), and <em>B</em><sup>2</sup>Σ<sub>u</sub><sup>+</sup> (green curve) states of N<sub>2</sub><sup>+</sup>.

- The nuclear wave packet moves around the minimal of the potential after the end of tunneling at <em>t</em> = 12 fs.

- Difference in the nuclear motion of the respective states leading to a varying electronic coherence which is proportional to the nuclear overlap.

- After around <em>t</em> = 20 fs, the nuclear wave packet of the <em>A</em><sup>2</sup>Π<sub>u</sub> state has little overlap with the other two states, so that the electron motion pauses.

- As nuclear wave packets overlap well at a later time, the electron motion resumes.

- This kind of dynamics occur for other diatomic molecules after ionization. But for polyatomic molecules, some nuclear wave packets may not return close to the equilibrium position.

## Controlling the electronic coherence
{: .cf}
- C.H. Yuen, Enhanced excited-state population and coherence via adiabatic tunneling ionization and excitation, Physical Review A 113 (1), 013125 (2026)

## Probing electronic coherence in molecules

- C.H. Yuen and C.D. Lin, Rotation in attosecond vibronic coherence spectroscopy for molecules, Communications Physics 7 (1) (2024)

- C.H. Yuen and C.D. Lin, Theory of strong-field sequential double ionization of polyatomic molecules, Physical Review A 109 (3), 033108 (2024)

- C.H. Yuen and C.D. Lin, Probing vibronic coherence in charge migration in molecules using strong-field sequential double ionization, Physical Review A 109 (1), L011101 (2024)
