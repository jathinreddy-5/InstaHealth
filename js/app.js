/**
 * InstaHealth - Client Application Controller
 * Manages watch UI rendering, carousel gestures, profile modal, and simulation events.
 * Zero-cloud, local-only execution.
 */

// Service Worker Registration for Offline PWA
if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('./sw.js').catch(() => {});
  });
}

(function () {
  'use strict';

  const engine = new InstaHealthEngine.HealthEngine();

  // UI Elements
  const btnOpenChangePerson = document.getElementById('btnOpenChangePerson');
  const changePersonModal = document.getElementById('changePersonModal');
  const btnCloseModal = document.getElementById('btnCloseModal');
  const savedProfilesList = document.getElementById('savedProfilesList');
  const emojiGrid = document.getElementById('emojiGrid');
  const btnSexMale = document.getElementById('btnSexMale');
  const btnSexFemale = document.getElementById('btnSexFemale');
  const modalInputAge = document.getElementById('modalInputAge');
  const modalValAge = document.getElementById('modalValAge');
  const btnSavePerson = document.getElementById('btnSavePerson');

  const dispActiveEmoji = document.getElementById('dispActiveEmoji');
  const dispActivePersonTitle = document.getElementById('dispActivePersonTitle');
  const dispActivePersonSub = document.getElementById('dispActivePersonSub');

  const dispTimelineBadge = document.getElementById('dispTimelineBadge');
  const timelineSection = document.getElementById('timelineSection');
  const stepDay1 = document.getElementById('stepDay1');
  const stepDay2 = document.getElementById('stepDay2');
  const stepDay3 = document.getElementById('stepDay3');
  const btnAdvanceDay = document.getElementById('btnAdvanceDay');
  const btnResetTimeline = document.getElementById('btnResetTimeline');

  const calibratingSection = document.getElementById('calibratingSection');
  const dispCalibratingText = document.getElementById('dispCalibratingText');
  const dispCalDayNum = document.getElementById('dispCalDayNum');
  const dispCohortBadge = document.getElementById('dispCohortBadge');
  const cmpRHRHuman = document.getElementById('cmpRHRHuman');
  const cmpRHRYou = document.getElementById('cmpRHRYou');
  const cmpStepsHuman = document.getElementById('cmpStepsHuman');
  const cmpStepsYou = document.getElementById('cmpStepsYou');
  const cmpSleepHuman = document.getElementById('cmpSleepHuman');
  const cmpSleepYou = document.getElementById('cmpSleepYou');
  const cmpCalHuman = document.getElementById('cmpCalHuman');
  const cmpCalYou = document.getElementById('cmpCalYou');
  const recommendationsSection = document.getElementById('recommendationsSection');

  const recSleepVal = document.getElementById('recSleepVal');
  const recSleepSub = document.getElementById('recSleepSub');
  const recStepVal = document.getElementById('recStepVal');
  const recStepSub = document.getElementById('recStepSub');
  const recSitVal = document.getElementById('recSitVal');
  const recSitSub = document.getElementById('recSitSub');
  const recCardioVal = document.getElementById('recCardioVal');
  const recCardioSub = document.getElementById('recCardioSub');

  const dispHealthScore = document.getElementById('dispHealthScore');
  const dispRingLabel = document.getElementById('dispRingLabel');
  const strainRing = document.getElementById('strainRingProgress');
  const dispCategory = document.getElementById('dispCategory');
  const dispDelta = document.getElementById('dispDelta');

  // Carousel Elements
  const ringCarousel = document.getElementById('ringCarousel');
  const carouselDots = document.querySelectorAll('.carousel-dot');

  // Slide 1: Sleep
  const sleepRingProgress = document.getElementById('sleepRingProgress');
  const dispSleepScore = document.getElementById('dispSleepScore');
  const dispSleepRingLabel = document.getElementById('dispSleepRingLabel');
  const dispSleepDelta = document.getElementById('dispSleepDelta');

  // Slide 2: Steps
  const stepRingProgress = document.getElementById('stepRingProgress');
  const dispStepScore = document.getElementById('dispStepScore');
  const dispStepRingLabel = document.getElementById('dispStepRingLabel');
  const dispStepDelta = document.getElementById('dispStepDelta');

  // Slide 3: Sit Still
  const sitRingProgress = document.getElementById('sitRingProgress');
  const dispSitScore = document.getElementById('dispSitScore');
  const dispSitRingLabel = document.getElementById('dispSitRingLabel');
  const dispSitDelta = document.getElementById('dispSitDelta');

  // Slide 4: Active Calories
  const calRingProgress = document.getElementById('calRingProgress');
  const dispCalScore = document.getElementById('dispCalScore');
  const dispCalRingLabel = document.getElementById('dispCalRingLabel');
  const dispCalDelta = document.getElementById('dispCalDelta');

  const dispMaxHR = document.getElementById('dispMaxHR');
  const dispRestingHR = document.getElementById('dispRestingHR');
  const dispCalories = document.getElementById('dispCalories');
  const dispRecovery = document.getElementById('dispRecovery');

  // Body Activity Ranges Elements
  const dispRangesTitle = document.getElementById('dispRangesTitle');
  const dispRHRRangeText = document.getElementById('dispRHRRangeText');
  const zoneRHR = document.getElementById('zoneRHR');
  const dotRHR = document.getElementById('dotRHR');
  const dispCalRangeText = document.getElementById('dispCalRangeText');
  const zoneCal = document.getElementById('zoneCal');
  const dotCal = document.getElementById('dotCal');
  const dispStrainRangeText = document.getElementById('dispStrainRangeText');
  const zoneStrain = document.getElementById('zoneStrain');
  const dotStrain = document.getElementById('dotStrain');

  const btnToggleBezel = document.getElementById('btnToggleBezel');
  const watchBezel = document.getElementById('watchBezel');

  // State for modal inputs
  let selectedEmoji = '🏃‍♂️';
  let selectedSex = 'male';
  let selectedAge = 24;

  // Workout State
  let currentWorkout = {
    durationMins: 30,
    activeCalories: 140,
    avgHR: 110,
    steps: 3200,
    perceivedExertion: 4
  };

  const PRESETS = {
    walk: { durationMins: 30, activeCalories: 140, avgHR: 110, steps: 3200, perceivedExertion: 4 },
    run: { durationMins: 45, activeCalories: 460, avgHR: 152, steps: 6100, perceivedExertion: 8 },
    hiit: { durationMins: 35, activeCalories: 380, avgHR: 162, steps: 2800, perceivedExertion: 9 },
    rest: { durationMins: 20, activeCalories: 60, avgHR: 85, steps: 1400, perceivedExertion: 2 }
  };

  // Watch Clock
  function updateClock() {
    const now = new Date();
    const hrs = String(now.getHours()).padStart(2, '0');
    const mins = String(now.getMinutes()).padStart(2, '0');
    const clockEl = document.getElementById('watchClock');
    if (clockEl) {
      clockEl.textContent = `${hrs}:${mins}`;
    }
  }
  setInterval(updateClock, 1000);
  updateClock();

  // Render Saved Profiles list inside modal
  function renderSavedProfiles() {
    if (!savedProfilesList) return;
    savedProfilesList.innerHTML = '';
    const profiles = engine.getProfiles();
    const activeId = engine.activeProfileId;

    profiles.forEach(p => {
      const chip = document.createElement('div');
      chip.className = `saved-profile-chip ${p.id === activeId ? 'active' : ''}`;
      chip.innerHTML = `<span>${p.emoji}</span> <span>${p.age}y ${p.sex === 'female' ? 'F' : 'M'} (Day ${p.currentDay || 1})</span>`;
      chip.addEventListener('click', () => {
        engine.switchProfile(p.id);
        closeModal();
        recalculate();
      });
      savedProfilesList.appendChild(chip);
    });
  }

  // Open Modal
  function openModal() {
    if (!changePersonModal) return;
    const active = engine.getActiveProfile();
    selectedEmoji = active.emoji || '🏃‍♂️';
    selectedSex = active.sex || 'male';
    selectedAge = active.age || 24;

    // Highlight selected emoji
    document.querySelectorAll('.emoji-option').forEach(el => {
      el.classList.toggle('selected', el.dataset.emoji === selectedEmoji);
    });

    // Set sex buttons
    if (btnSexMale && btnSexFemale) {
      btnSexMale.classList.toggle('selected', selectedSex === 'male');
      btnSexFemale.classList.toggle('selected', selectedSex === 'female');
    }

    // Set age slider
    if (modalInputAge && modalValAge) {
      modalInputAge.value = selectedAge;
      modalValAge.textContent = `${selectedAge} yrs`;
    }

    renderSavedProfiles();
    changePersonModal.classList.add('active');
  }

  function closeModal() {
    if (changePersonModal) {
      changePersonModal.classList.remove('active');
    }
  }

  // Emoji Selection Listener
  if (emojiGrid) {
    emojiGrid.addEventListener('click', (e) => {
      const item = e.target.closest('.emoji-option');
      if (!item) return;
      document.querySelectorAll('.emoji-option').forEach(el => el.classList.remove('selected'));
      item.classList.add('selected');
      selectedEmoji = item.dataset.emoji;
    });
  }

  // Sex Selection Listeners
  if (btnSexMale) {
    btnSexMale.addEventListener('click', () => {
      selectedSex = 'male';
      btnSexMale.classList.add('selected');
      if (btnSexFemale) btnSexFemale.classList.remove('selected');
    });
  }
  if (btnSexFemale) {
    btnSexFemale.addEventListener('click', () => {
      selectedSex = 'female';
      btnSexFemale.classList.add('selected');
      if (btnSexMale) btnSexMale.classList.remove('selected');
    });
  }

  // Age Slider Listener
  if (modalInputAge && modalValAge) {
    modalInputAge.addEventListener('input', (e) => {
      selectedAge = Number(e.target.value);
      modalValAge.textContent = `${selectedAge} yrs`;
    });
  }

  // Save Person Button
  if (btnSavePerson) {
    btnSavePerson.addEventListener('click', () => {
      engine.addOrUpdateProfile({
        emoji: selectedEmoji,
        sex: selectedSex,
        age: selectedAge
      });
      closeModal();
      recalculate();
    });
  }

  // Advance Day Automatically (Auto-Wear 24h)
  if (btnAdvanceDay) {
    btnAdvanceDay.addEventListener('click', () => {
      btnAdvanceDay.textContent = '⏳ Simulating 24h Wear...';
      btnAdvanceDay.style.opacity = '0.7';
      setTimeout(() => {
        engine.advanceDay(currentWorkout);
        recalculate();
        btnAdvanceDay.textContent = '⏩ Advance Day [Simulation Demo]';
        btnAdvanceDay.style.opacity = '1';
      }, 150);
    });
  }

  // Reset Timeline
  if (btnResetTimeline) {
    btnResetTimeline.addEventListener('click', () => {
      if (confirm('Restart 2-Day Calibration for this person?')) {
        engine.resetTimeline();
        recalculate();
      }
    });
  }

  if (btnOpenChangePerson) btnOpenChangePerson.addEventListener('click', openModal);
  if (btnCloseModal) btnCloseModal.addEventListener('click', closeModal);

  // Recalculate and update the watch view
  function recalculate() {
    const res = engine.calculateCondition(currentWorkout);
    const person = res.person;
    const ranges = res.trainedRanges;
    const recs = res.recommendations;
    const currentDay = person.currentDay || engine.profile.currentDay || 1;

    // Top Person Header Bar
    if (dispActiveEmoji) dispActiveEmoji.textContent = person.emoji;
    if (dispActivePersonTitle) dispActivePersonTitle.textContent = `${person.emoji} Profile`;
    if (dispActivePersonSub) dispActivePersonSub.textContent = `${person.sex === 'female' ? 'Female' : 'Male'} · ${person.age} yrs · ${person.restingHR} bpm`;

    // Timeline Step Badges
    if (dispTimelineBadge) {
      dispTimelineBadge.textContent = recs.isCalibrated ? '✅ Calibrated' : `Day ${currentDay} of 2`;
      dispTimelineBadge.style.color = recs.isCalibrated ? 'var(--accent-green)' : 'var(--accent-purple)';
    }

    if (stepDay1) stepDay1.className = `timeline-step ${currentDay === 1 ? 'active' : 'completed'}`;
    if (stepDay2) stepDay2.className = `timeline-step ${currentDay === 2 ? 'active' : (currentDay > 2 ? 'completed' : '')}`;
    if (stepDay3) stepDay3.className = `timeline-step ${currentDay >= 3 ? 'completed active' : ''}`;

    // Toggle Calibration Notice vs Personalized Prescriptions
    const humanAvg = recs.humanAverages || {
      cohortLabel: `${person.age}y ${person.sex === 'female' ? 'Female' : 'Male'}`,
      restingHR: person.sex === 'female' ? 62 : 60,
      steps: 8000,
      sleepHours: 7.8,
      burnRateCalHr: 360
    };
    const personData = recs.personCurrent || humanAvg;

    if (!recs.isCalibrated) {
      if (timelineSection) timelineSection.style.display = 'flex';
      if (calibratingSection) calibratingSection.style.display = 'flex';
      if (recommendationsSection) recommendationsSection.style.display = 'none';

      if (dispCalDayNum) dispCalDayNum.textContent = currentDay;
      if (dispCohortBadge) dispCohortBadge.textContent = `${humanAvg.cohortLabel} Baseline`;

      // 1. Resting HR Comparison
      if (cmpRHRHuman) cmpRHRHuman.textContent = `${humanAvg.restingHR} bpm`;
      if (cmpRHRYou) cmpRHRYou.textContent = `${personData.restingHR} bpm`;

      // 2. Steps Comparison
      if (cmpStepsHuman) cmpStepsHuman.textContent = `${humanAvg.steps.toLocaleString()}`;
      if (cmpStepsYou) cmpStepsYou.textContent = `${personData.steps.toLocaleString()}`;

      // 3. Sleep Comparison
      if (cmpSleepHuman) cmpSleepHuman.textContent = `${humanAvg.sleepHours}h`;
      if (cmpSleepYou) cmpSleepYou.textContent = `${personData.sleepHours}h`;

      // 4. Calorie Burn Comparison
      if (cmpCalHuman) cmpCalHuman.textContent = `${humanAvg.burnRateCalHr} cal/hr`;
      if (cmpCalYou) cmpCalYou.textContent = `${personData.burnRateCalHr} cal/hr`;

      if (dispCalibratingText) {
        dispCalibratingText.textContent = currentDay === 1
          ? `Day 1: Baseline Initialized · Day 3 unlocks custom plan`
          : `Day 2: Analyzing Personal Data Separately · Tomorrow unlocks custom plan`;
      }
      
      // Ring shows Calibration Readiness Progress
      if (dispHealthScore) dispHealthScore.textContent = `${recs.progressPercent}%`;
      if (dispRingLabel) dispRingLabel.textContent = currentDay === 1 ? 'Baseline Set' : 'Calibrating';
      if (strainRing) strainRing.style.stroke = 'var(--accent-purple)';
    } else {
      if (timelineSection) timelineSection.style.display = 'none';
      if (calibratingSection) calibratingSection.style.display = 'none';
      if (recommendationsSection) recommendationsSection.style.display = 'flex';

      // Ring shows Cardiorespiratory Readiness Score (> baseline)
      if (dispHealthScore) dispHealthScore.textContent = `${recs.cardioReadiness.score}%`;
      if (dispRingLabel) dispRingLabel.textContent = 'Cardio Ready';
      if (strainRing) strainRing.style.stroke = recs.cardioReadiness.color;

      // Fill Recommendations (> firstly trained data)
      if (recSleepVal) recSleepVal.textContent = recs.sleep.formatted;
      if (recSleepSub) recSleepSub.textContent = 'Recovery Goal';

      if (recStepVal) recStepVal.textContent = recs.steps.formatted;
      if (recStepSub) recStepSub.textContent = 'Daily Target';

      if (recSitVal) recSitVal.textContent = recs.sitStill.formatted;
      if (recSitSub) recSitSub.textContent = 'Max Stillness';

      if (recCardioVal) {
        recCardioVal.textContent = `${recs.cardioReadiness.score}%`;
        recCardioVal.style.color = recs.cardioReadiness.color;
      }
      if (recCardioSub) recCardioSub.textContent = recs.cardioReadiness.status;
    }

    // Circular Rings Calculation for Carousel (Slides 0-4)
    const circumference = 345.57;

    // 1. Slide 0: Cardio Readiness Score
    const scoreVal = recs.isCalibrated ? recs.cardioReadiness.score : (currentDay === 1 ? 85 : 88);
    const fraction0 = Math.min(1.0, scoreVal / 100.0);
    if (strainRing) strainRing.style.strokeDashoffset = circumference - (fraction0 * circumference);

    // 2. Slide 1: Sleep Need
    let targetSleepHours = 8.0;
    let hoursSlept = 7.8;
    if (recs.isCalibrated && recs.sleep) {
      targetSleepHours = recs.sleep.targetHours || Number((recs.sleep.hours + (recs.sleep.minutes / 60)).toFixed(1));
      hoursSlept = (person.historyDays && person.historyDays.length > 0)
        ? Number((person.historyDays[person.historyDays.length - 1].sleepHours || targetSleepHours).toFixed(1))
        : targetSleepHours;
      if (dispSleepRingLabel) dispSleepRingLabel.textContent = `/ ${targetSleepHours}h NEEDED`;
      if (dispSleepDelta) {
        dispSleepDelta.innerHTML = `<strong>${hoursSlept}h</strong> slept / <strong>${targetSleepHours}h</strong> goal`;
      }
    } else {
      targetSleepHours = humanAvg.sleepHours;
      hoursSlept = personData.sleepHours;
      if (dispSleepRingLabel) {
        dispSleepRingLabel.textContent = `/ ${targetSleepHours}h NEEDED`;
      }
      if (dispSleepDelta) {
        dispSleepDelta.innerHTML = `<strong>${hoursSlept}h</strong> slept of <strong>${targetSleepHours}h</strong> goal`;
      }
    }

    if (dispSleepScore) dispSleepScore.textContent = `${hoursSlept}h`;
    const sleepFraction = Math.min(1.0, hoursSlept / Math.max(1, targetSleepHours));
    if (sleepRingProgress) sleepRingProgress.style.strokeDashoffset = circumference - (sleepFraction * circumference);

    // 3. Slide 2: Steps Goal
    let targetSteps = 8000;
    let stepsWalked = 8000;
    if (recs.isCalibrated && recs.steps) {
      targetSteps = recs.steps.target;
      stepsWalked = (person.historyDays && person.historyDays.length > 0)
        ? person.historyDays[person.historyDays.length - 1].steps
        : targetSteps;
      if (dispStepRingLabel) dispStepRingLabel.textContent = `/ ${(targetSteps / 1000).toFixed(1)}k STEPS`;
      if (dispStepDelta) {
        dispStepDelta.innerHTML = `<strong>${stepsWalked.toLocaleString()}</strong> / <strong>${targetSteps.toLocaleString()}</strong> steps`;
      }
    } else {
      targetSteps = humanAvg.steps;
      stepsWalked = personData.steps;
      if (dispStepRingLabel) {
        dispStepRingLabel.textContent = `/ ${(targetSteps / 1000).toFixed(1)}k STEPS`;
      }
      if (dispStepDelta) {
        dispStepDelta.innerHTML = `<strong>${stepsWalked.toLocaleString()}</strong> of <strong>${targetSteps.toLocaleString()}</strong> steps`;
      }
    }

    if (dispStepScore) dispStepScore.textContent = stepsWalked >= 1000 ? `${(stepsWalked / 1000).toFixed(1)}k` : `${stepsWalked}`;
    const stepFraction = Math.min(1.0, stepsWalked / Math.max(1, targetSteps));
    if (stepRingProgress) stepRingProgress.style.strokeDashoffset = circumference - (stepFraction * circumference);

    // 4. Slide 3: Sit Still Inactivity Limit
    const maxSitMins = recs.isCalibrated && recs.sitStill ? recs.sitStill.maxMins : (person.age >= 60 ? 40 : 55);
    const currentSitMins = Math.round(maxSitMins * 0.65);
    if (dispSitScore) dispSitScore.textContent = `${currentSitMins}m`;
    if (dispSitRingLabel) dispSitRingLabel.textContent = `/ ${maxSitMins}m STILL`;
    if (dispSitDelta) {
      dispSitDelta.innerHTML = `<strong>${currentSitMins}m</strong> still / <strong>${maxSitMins}m</strong> limit`;
    }
    const sitFraction = Math.min(1.0, currentSitMins / maxSitMins);
    if (sitRingProgress) sitRingProgress.style.strokeDashoffset = circumference - (sitFraction * circumference);

    // 5. Slide 4: Active Calories Burn
    let targetCalories = 360;
    let currentCal = 360;
    if (recs.isCalibrated && recs.activeCalories) {
      targetCalories = recs.activeCalories.target;
      currentCal = (person.historyDays && person.historyDays.length > 0)
        ? person.historyDays[person.historyDays.length - 1].activeCalories
        : targetCalories;
      if (dispCalRingLabel) dispCalRingLabel.textContent = `/ ${targetCalories} KCAL`;
      if (dispCalDelta) {
        dispCalDelta.innerHTML = `<strong>${currentCal}</strong> of <strong>${targetCalories}</strong> kcal goal`;
      }
    } else {
      targetCalories = humanAvg.burnRateCalHr;
      currentCal = personData.burnRateCalHr;
      if (dispCalRingLabel) {
        dispCalRingLabel.textContent = `/ ${targetCalories} KCAL`;
      }
      if (dispCalDelta) {
        dispCalDelta.innerHTML = `<strong>${currentCal}</strong> of <strong>${targetCalories}</strong> kcal goal`;
      }
    }

    if (dispCalScore) dispCalScore.textContent = `${currentCal}`;
    const calFraction = Math.min(1.0, currentCal / Math.max(1, targetCalories));
    if (calRingProgress) calRingProgress.style.strokeDashoffset = circumference - (calFraction * circumference);

    // Status badges
    if (dispCategory) {
      dispCategory.textContent = res.category;
      dispCategory.style.color = res.categoryColor;
      dispCategory.style.background = res.categoryColor + '22';
    }

    const sign = res.personalDelta > 0 ? '+' : '';
    if (dispDelta) {
      dispDelta.innerHTML = `Strain: <strong>${res.strain} / 21</strong>`;
    }

    // Vitals Grid
    if (dispMaxHR) dispMaxHR.textContent = `${res.metrics.maxHR} bpm`;
    if (dispRestingHR) dispRestingHR.textContent = `${res.metrics.restingHR} bpm`;
    if (dispCalories) dispCalories.textContent = `${res.metrics.activeCalories} kcal`;
    if (dispRecovery) dispRecovery.textContent = `${res.recoveryHours} hrs`;

    // Body Activity Card Title Update
    if (dispRangesTitle) dispRangesTitle.textContent = `${person.emoji} Body Activity`;

    // 1. Resting HR Range
    if (dispRHRRangeText) dispRHRRangeText.textContent = `${ranges.restingHR.min} – ${ranges.restingHR.max} bpm`;
    const rhrMinPct = Math.max(0, Math.min(100, ((ranges.restingHR.min - 40) / 60) * 100));
    const rhrMaxPct = Math.max(0, Math.min(100, ((ranges.restingHR.max - 40) / 60) * 100));
    const rhrCurPct = Math.max(0, Math.min(100, ((res.metrics.restingHR - 40) / 60) * 100));
    if (zoneRHR) {
      zoneRHR.style.left = `${rhrMinPct}%`;
      zoneRHR.style.width = `${Math.max(4, rhrMaxPct - rhrMinPct)}%`;
    }
    if (dotRHR) dotRHR.style.left = `${rhrCurPct}%`;

    // 2. Active Calories Range
    if (dispCalRangeText) dispCalRangeText.textContent = `${ranges.activeCalories.min} – ${ranges.activeCalories.max} cal/hr`;
    const calMinPct = Math.max(0, Math.min(100, ((ranges.activeCalories.min - 100) / 450) * 100));
    const calMaxPct = Math.max(0, Math.min(100, ((ranges.activeCalories.max - 100) / 450) * 100));
    const curHourlyBurn = Math.round((res.metrics.activeCalories / res.metrics.durationMins) * 60);
    const calCurPct = Math.max(0, Math.min(100, ((curHourlyBurn - 100) / 450) * 100));
    if (zoneCal) {
      zoneCal.style.left = `${calMinPct}%`;
      zoneCal.style.width = `${Math.max(4, calMaxPct - calMinPct)}%`;
    }
    if (dotCal) dotCal.style.left = `${calCurPct}%`;

    // 3. Strain Tolerance Range
    if (dispStrainRangeText) dispStrainRangeText.textContent = `${ranges.dailyStrain.min} – ${ranges.dailyStrain.max} pts`;
    const strainMinPct = Math.max(0, Math.min(100, (ranges.dailyStrain.min / 21) * 100));
    const strainMaxPct = Math.max(0, Math.min(100, (ranges.dailyStrain.max / 21) * 100));
    const strainCurPct = Math.max(0, Math.min(100, (res.strain / 21) * 100));
    if (zoneStrain) {
      zoneStrain.style.left = `${strainMinPct}%`;
      zoneStrain.style.width = `${Math.max(4, strainMaxPct - strainMinPct)}%`;
    }
    if (dotStrain) dotStrain.style.left = `${strainCurPct}%`;
  }

  // Presets
  document.querySelectorAll('.btn-preset').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.btn-preset').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      const presetKey = btn.dataset.preset;
      currentWorkout = { ...PRESETS[presetKey] };
      recalculate();
    });
  });

  // Bezel view toggle
  if (btnToggleBezel && watchBezel) {
    btnToggleBezel.addEventListener('click', () => {
      const isFullscreen = watchBezel.classList.toggle('fullscreen-mode');
      btnToggleBezel.textContent = isFullscreen ? 'Switch to Bezel View' : 'Switch to Watch View';
    });
  }

  // Ring Carousel Horizontal Swipe, Drag & Dot Pagination
  function updateActiveCarouselDot() {
    if (!ringCarousel) return;
    const slideWidth = ringCarousel.offsetWidth;
    if (!slideWidth) return;
    const activeIdx = Math.round(ringCarousel.scrollLeft / slideWidth);
    carouselDots.forEach((dot, idx) => {
      dot.classList.toggle('active', idx === activeIdx);
    });
  }

  if (ringCarousel) {
    ringCarousel.addEventListener('scroll', updateActiveCarouselDot, { passive: true });
  }

  carouselDots.forEach((dot) => {
    dot.addEventListener('click', () => {
      if (!ringCarousel) return;
      const idx = Number(dot.dataset.index);
      const slideWidth = ringCarousel.offsetWidth;
      ringCarousel.scrollTo({
        left: idx * slideWidth,
        behavior: 'smooth'
      });
    });
  });

  // Mouse drag to swipe (for desktop testing)
  let isDraggingCarousel = false;
  let startDragX = 0;
  let startCarouselScroll = 0;

  if (ringCarousel) {
    ringCarousel.addEventListener('mousedown', (e) => {
      isDraggingCarousel = true;
      startDragX = e.pageX - ringCarousel.offsetLeft;
      startCarouselScroll = ringCarousel.scrollLeft;
    });

    window.addEventListener('mouseup', () => {
      if (!isDraggingCarousel) return;
      isDraggingCarousel = false;
      const slideWidth = ringCarousel.offsetWidth;
      const targetIdx = Math.round(ringCarousel.scrollLeft / slideWidth);
      ringCarousel.scrollTo({
        left: targetIdx * slideWidth,
        behavior: 'smooth'
      });
    });

    ringCarousel.addEventListener('mousemove', (e) => {
      if (!isDraggingCarousel) return;
      e.preventDefault();
      const currentX = e.pageX - ringCarousel.offsetLeft;
      const walk = (currentX - startDragX) * 1.2;
      ringCarousel.scrollLeft = startCarouselScroll - walk;
    });
  }

  // Initial run
  recalculate();
})();
