/* ==========================================================================
   HASS Online Learning Program — shared lesson behaviour
   Plain JS, no build step, no dependencies. Loaded by every lesson page.

   Provides, all driven by data-attributes so lesson HTML stays declarative:
   - Tabs                          [data-tabs] / [data-tab] / .tab-panel
   - localStorage autosave         [data-autosave="key"]
   - Paste-disabled CER boxes      [data-no-paste]
   - Auto-marked multiple choice   [data-mcq] / [data-choice] / [data-correct]
   - Reveal locked until unlocked  [data-reveal-trigger] / [data-unlock-from]
   - Download my answers           [data-download-answers]
   ========================================================================== */

(function () {
  "use strict";

  var STORAGE_PREFIX = "hass:" + location.pathname + ":";

  function storageKey(key) {
    return STORAGE_PREFIX + key;
  }

  /* ------------------------------------------------------------------
     Tabs
     ------------------------------------------------------------------ */

  function initTabs() {
    document.querySelectorAll("[data-tabs]").forEach(function (group) {
      var buttons = group.querySelectorAll(".tab-btn");
      var panels = group.querySelectorAll(".tab-panel");

      function activate(name) {
        buttons.forEach(function (b) {
          var isActive = b.getAttribute("data-tab") === name;
          b.setAttribute("aria-selected", isActive ? "true" : "false");
        });
        panels.forEach(function (p) {
          p.classList.toggle("-active", p.id === name);
        });
      }

      buttons.forEach(function (b) {
        b.addEventListener("click", function () {
          activate(b.getAttribute("data-tab"));
        });
      });

      if (buttons.length) {
        activate(buttons[0].getAttribute("data-tab"));
      }
    });
  }

  /* ------------------------------------------------------------------
     Autosave (textareas and other [data-autosave] fields)
     ------------------------------------------------------------------ */

  function initAutosave() {
    document.querySelectorAll("[data-autosave]").forEach(function (field) {
      var key = field.getAttribute("data-autosave");
      var statusEl = document.querySelector('[data-save-status-for="' + key + '"]');
      var saved = localStorage.getItem(storageKey(key));

      if (saved !== null) {
        field.value = saved;
      }

      var timer = null;
      field.addEventListener("input", function () {
        clearTimeout(timer);
        if (statusEl) statusEl.textContent = "";
        timer = setTimeout(function () {
          localStorage.setItem(storageKey(key), field.value);
          if (statusEl) {
            statusEl.textContent = "Saved";
            setTimeout(function () {
              if (statusEl.textContent === "Saved") statusEl.textContent = "";
            }, 2000);
          }
          checkUnlocks();
        }, 400);
      });
    });
  }

  /* ------------------------------------------------------------------
     Paste-disabled fields (CER responses)
     ------------------------------------------------------------------ */

  function initNoPaste() {
    document.querySelectorAll("[data-no-paste]").forEach(function (field) {
      field.addEventListener("paste", function (e) {
        e.preventDefault();
      });
    });
  }

  /* ------------------------------------------------------------------
     Multiple choice, auto-marked
     ------------------------------------------------------------------ */

  function initMcq() {
    document.querySelectorAll("[data-mcq]").forEach(function (mcq) {
      var options = mcq.querySelectorAll("[data-choice]");
      var feedback = mcq.querySelector(".mcq-feedback");
      var key = mcq.getAttribute("data-autosave-key");

      function markAnswered(choiceEl) {
        var correct = choiceEl.getAttribute("data-choice") === mcq.getAttribute("data-correct");

        options.forEach(function (o) {
          o.disabled = true;
          if (o.getAttribute("data-choice") === mcq.getAttribute("data-correct")) {
            o.classList.add("-correct");
          }
        });

        if (!correct) {
          choiceEl.classList.add("-incorrect");
        }

        if (feedback) {
          feedback.textContent = correct
            ? mcq.getAttribute("data-feedback-correct") || "Correct."
            : mcq.getAttribute("data-feedback-incorrect") || "Not quite — check the correct answer above.";
          feedback.classList.add(correct ? "-correct" : "-incorrect");
        }

        mcq.classList.add("-answered");

        if (key) {
          localStorage.setItem(storageKey(key), choiceEl.getAttribute("data-choice"));
        }

        checkUnlocks();
      }

      options.forEach(function (o) {
        o.addEventListener("click", function () {
          if (mcq.classList.contains("-answered")) return;
          markAnswered(o);
        });
      });

      // Restore a previous answer on reload.
      if (key) {
        var saved = localStorage.getItem(storageKey(key));
        if (saved !== null) {
          var match = mcq.querySelector('[data-choice="' + saved + '"]');
          if (match) markAnswered(match);
        }
      }
    });
  }

  /* ------------------------------------------------------------------
     Reveal, locked until the linked step has been interacted with
     ------------------------------------------------------------------ */

  function isUnlocked(sourceId) {
    var source = document.getElementById(sourceId);
    if (!source) return true;

    if (source.hasAttribute("data-mcq")) {
      return source.classList.contains("-answered");
    }

    if ("value" in source) {
      return source.value.trim().length > 0;
    }

    return true;
  }

  function checkUnlocks() {
    document.querySelectorAll("[data-reveal-trigger]").forEach(function (btn) {
      var sourceId = btn.getAttribute("data-unlock-from");
      var unlocked = !sourceId || isUnlocked(sourceId);
      btn.disabled = !unlocked;
    });
  }

  function initReveals() {
    document.querySelectorAll("[data-reveal-trigger]").forEach(function (btn) {
      var targetId = btn.getAttribute("data-reveal-trigger");
      btn.addEventListener("click", function () {
        var target = document.getElementById(targetId);
        if (target) target.hidden = false;
        btn.hidden = true;
      });
    });

    document.querySelectorAll("[data-unlock-from]").forEach(function (btn) {
      var sourceId = btn.getAttribute("data-unlock-from");
      var source = document.getElementById(sourceId);
      if (source && "addEventListener" in source) {
        source.addEventListener("input", checkUnlocks);
      }
    });

    checkUnlocks();
  }

  /* ------------------------------------------------------------------
     Download my answers
     ------------------------------------------------------------------ */

  function initDownload() {
    var btn = document.querySelector("[data-download-answers]");
    if (!btn) return;

    btn.addEventListener("click", function () {
      var lines = [
        document.title,
        "Downloaded: " + new Date().toLocaleString("en-AU"),
        "",
      ];

      document.querySelectorAll("[data-autosave]").forEach(function (field) {
        var label = field.getAttribute("data-label") || field.getAttribute("data-autosave");
        var value = field.value || "(no answer given)";
        lines.push("Q: " + label);
        lines.push("A: " + value);
        lines.push("");
      });

      document.querySelectorAll("[data-mcq]").forEach(function (mcq) {
        var label = mcq.getAttribute("data-label") || "Multiple choice";
        var answered = mcq.classList.contains("-answered");
        lines.push("Q: " + label);
        lines.push("A: " + (answered ? "answered" : "(not answered)"));
        lines.push("");
      });

      var blob = new Blob([lines.join("\n")], { type: "text/plain" });
      var url = URL.createObjectURL(blob);
      var a = document.createElement("a");
      a.href = url;
      a.download = (document.body.getAttribute("data-lesson-slug") || "my-answers") + ".txt";
      document.body.appendChild(a);
      a.click();
      a.remove();
      URL.revokeObjectURL(url);
    });
  }

  document.addEventListener("DOMContentLoaded", function () {
    initTabs();
    initAutosave();
    initNoPaste();
    initMcq();
    initReveals();
    initDownload();
  });
})();
