/* K7 KICKBOXING GYM — site script (no dependencies) */
(function () {
  "use strict";

  /* ------------------------------------------------------------------
     CONFIG — edit these two values when going live
     FORM_ENDPOINT: any service that accepts a JSON POST (Formspree,
     Getform, Basin, your own API). Leave empty to hand the enquiry
     over to WhatsApp / phone instead.
     ------------------------------------------------------------------ */
  var CONFIG = {
    FORM_ENDPOINT: "",
    WHATSAPP_NUMBER: "923482136361", // 0348 2136361 in international format
    PHONE_DISPLAY: "0348 2136361",
    TIMEZONE: "Asia/Karachi",
    OPEN_HOUR: 9,
    CLOSE_HOUR: 22
  };

  var doc = document.documentElement;
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---------- Load sequence ---------- */
  function loaded() { requestAnimationFrame(function () { doc.classList.add("is-loaded"); }); }
  if (document.readyState === "complete") loaded(); else window.addEventListener("load", loaded);
  // Safety: never keep the hero hidden if an image is slow
  setTimeout(function () { doc.classList.add("is-loaded"); }, 1600);

  /* ---------- Header state ---------- */
  var hdr = document.querySelector("[data-hdr]");
  var lastY = window.scrollY;
  var ticking = false;
  function onScroll() {
    var y = window.scrollY;
    if (hdr) {
      hdr.classList.toggle("is-scrolled", y > 40);
      var menuOpen = document.body.classList.contains("is-locked");
      hdr.classList.toggle("is-hidden", !menuOpen && y > 600 && y > lastY + 4);
      if (y < lastY - 4) hdr.classList.remove("is-hidden");
    }
    lastY = y;
    parallax();
    ticking = false;
  }
  window.addEventListener("scroll", function () {
    if (!ticking) { requestAnimationFrame(onScroll); ticking = true; }
  }, { passive: true });

  /* ---------- Mobile menu ---------- */
  var burger = document.querySelector(".burger");
  var menu = document.getElementById("menu");
  function setMenu(open) {
    if (!burger || !menu) return;
    burger.setAttribute("aria-expanded", String(open));
    burger.setAttribute("aria-label", open ? "Close menu" : "Open menu");
    menu.classList.toggle("is-open", open);
    menu.toggleAttribute("inert", !open);
    menu.setAttribute("aria-hidden", String(!open));
    document.body.classList.toggle("is-locked", open);
    if (hdr) hdr.classList.remove("is-hidden");
    if (open) {
      var first = menu.querySelector("a");
      if (first) setTimeout(function () { first.focus(); }, 300);
    } else {
      burger.focus();
    }
  }
  if (burger && menu) {
    menu.setAttribute("inert", "");
    burger.addEventListener("click", function () { setMenu(burger.getAttribute("aria-expanded") !== "true"); });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && menu.classList.contains("is-open")) setMenu(false);
      // keep focus inside the open menu
      if (e.key === "Tab" && menu.classList.contains("is-open")) {
        var f = [burger].concat(Array.prototype.slice.call(menu.querySelectorAll("a, button")));
        var i = f.indexOf(document.activeElement);
        if (e.shiftKey && i <= 0) { e.preventDefault(); f[f.length - 1].focus(); }
        else if (!e.shiftKey && i === f.length - 1) { e.preventDefault(); f[0].focus(); }
      }
    });
    menu.addEventListener("click", function (e) { if (e.target.closest("a")) setMenu(false); });
    window.addEventListener("resize", function () { if (window.innerWidth > 1080 && menu.classList.contains("is-open")) setMenu(false); });
  }

  /* ---------- Reveal on scroll ---------- */
  var revealables = Array.prototype.filter.call(document.querySelectorAll(".rv, .rv-img, .lines"), function (el) { return !el.closest(".hero"); });
  if ("IntersectionObserver" in window && !reduce) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add("in"); io.unobserve(en.target); }
      });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.12 });
    revealables.forEach(function (el) { io.observe(el); });
  } else {
    revealables.forEach(function (el) { el.classList.add("in"); });
  }

  /* ---------- Parallax ---------- */
  var px = reduce ? [] : Array.prototype.slice.call(document.querySelectorAll("[data-parallax]"));
  function parallax() {
    if (!px.length) return;
    var vh = window.innerHeight;
    px.forEach(function (el) {
      var r = el.parentElement.getBoundingClientRect();
      if (r.bottom < 0 || r.top > vh) return;
      var speed = parseFloat(el.getAttribute("data-parallax")) || 0.12;
      var p = (r.top + r.height / 2 - vh / 2) * speed;
      el.style.transform = "translate3d(0," + p.toFixed(1) + "px,0)";
    });
  }
  parallax();

  /* ---------- Hover preview for index lists ---------- */
  var list = document.querySelector("[data-hoverlist]");
  var prev = document.querySelector(".hoverprev");
  if (list && prev && window.matchMedia("(hover: hover) and (min-width: 901px)").matches) {
    var imgs = prev.querySelectorAll("img");
    var tx = 0, ty = 0, cx = 0, cy = 0, raf = null;
    function loop() {
      cx += (tx - cx) * 0.16; cy += (ty - cy) * 0.16;
      prev.style.transform = "translate3d(" + cx + "px," + cy + "px,0) translate(-50%,-50%) scale(" + (prev.classList.contains("is-on") ? 1 : .85) + ")";
      raf = requestAnimationFrame(loop);
    }
    list.addEventListener("mousemove", function (e) { tx = e.clientX + 170; ty = e.clientY; if (!raf) { cx = tx; cy = ty; loop(); } });
    list.querySelectorAll("[data-prev]").forEach(function (row) {
      row.addEventListener("mouseenter", function () {
        var k = row.getAttribute("data-prev");
        imgs.forEach(function (im) { im.classList.toggle("is-cur", im.getAttribute("data-k") === k); });
        prev.classList.add("is-on");
      });
    });
    list.addEventListener("mouseleave", function () {
      prev.classList.remove("is-on");
      setTimeout(function () { if (!prev.classList.contains("is-on") && raf) { cancelAnimationFrame(raf); raf = null; } }, 400);
    });
  }

  /* ---------- Live open / closed status (Karachi time) ---------- */
  function karachiNow() {
    try {
      var parts = new Intl.DateTimeFormat("en-GB", { timeZone: CONFIG.TIMEZONE, weekday: "short", hour: "2-digit", minute: "2-digit", hour12: false }).formatToParts(new Date());
      var o = {}; parts.forEach(function (p) { o[p.type] = p.value; });
      return { day: o.weekday, h: parseInt(o.hour, 10) % 24, m: parseInt(o.minute, 10) };
    } catch (e) { return null; }
  }
  function updateStatus() {
    var n = karachiNow(); if (!n) return;
    var isSun = n.day === "Sun";
    var open = !isSun && n.h >= CONFIG.OPEN_HOUR && n.h < CONFIG.CLOSE_HOUR;
    var text;
    if (open) text = "Open now — until 10:00 PM";
    else if (isSun) text = "Closed today — opens Monday 9:00 AM";
    else if (n.h < CONFIG.OPEN_HOUR) text = "Closed — opens today 9:00 AM";
    else text = n.day === "Sat" ? "Closed — opens Monday 9:00 AM" : "Closed — opens tomorrow 9:00 AM";
    document.querySelectorAll("[data-status]").forEach(function (el) {
      el.classList.toggle("is-open", open);
      var t = el.querySelector("[data-status-text]"); if (t) t.textContent = text;
    });
  }
  updateStatus(); setInterval(updateStatus, 60000);

  /* ---------- Programs: highlight active category ---------- */
  var catLinks = document.querySelectorAll(".catnav a");
  if (catLinks.length && "IntersectionObserver" in window) {
    var cio = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        catLinks.forEach(function (a) { a.classList.toggle("is-active", a.getAttribute("href") === "#" + en.target.id); });
      });
    }, { rootMargin: "-45% 0px -50% 0px" });
    document.querySelectorAll(".cat[id]").forEach(function (s) { cio.observe(s); });
  }

  /* ---------- Forms ---------- */
  var params = new URLSearchParams(window.location.search);
  document.querySelectorAll("form[data-enquiry]").forEach(function (form) {
    var select = form.querySelector("select[name=program]");
    var pre = params.get("program");
    if (select && pre) {
      Array.prototype.forEach.call(select.options, function (o) { if (o.value === pre) select.value = pre; });
    }

    var btn = form.querySelector("button[type=submit]");
    var btnLabel = btn ? btn.querySelector(".lbl") : null;
    var idleText = btnLabel ? btnLabel.textContent : "";
    var alertBox = form.querySelector(".form-alert");
    var wrap = form.closest("[data-form-wrap]");
    var okState = wrap ? wrap.querySelector(".fstate--ok") : null;
    var errState = wrap ? wrap.querySelector(".fstate--err") : null;

    function setErr(field, msg) {
      var box = field.closest(".field"); if (!box) return;
      var e = box.querySelector(".field__err");
      box.classList.toggle("has-error", !!msg);
      field.setAttribute("aria-invalid", msg ? "true" : "false");
      if (e) e.textContent = msg || "";
    }
    function validate(field) {
      var v = (field.value || "").trim(); var n = field.name;
      if (field.required && !v) {
        var lbl = { name: "Enter your name.", phone: "Enter a phone number so we can reach you.", program: "Choose the program you're interested in.", message: "Write a short message." }[n] || "This field is required.";
        setErr(field, lbl); return false;
      }
      if (n === "name" && v && v.length < 2) { setErr(field, "Enter your full name."); return false; }
      if (n === "phone" && v) {
        var digits = v.replace(/[^\d]/g, "");
        if (!/^[+\d][\d\s\-()]*$/.test(v) || digits.length < 10 || digits.length > 13) { setErr(field, "Enter a valid phone number, e.g. 0300 1234567."); return false; }
      }
      if (n === "email" && v && !/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v)) { setErr(field, "Enter a valid email address, e.g. name@example.com."); return false; }
      setErr(field, ""); return true;
    }
    form.querySelectorAll("input, select, textarea").forEach(function (f) {
      f.addEventListener("blur", function () { if (f.value) validate(f); });
      f.addEventListener("input", function () { if (f.closest(".field.has-error")) validate(f); });
    });

    function composeText(data) {
      var lines = ["Hello K7 Kickboxing Gym, I'd like to enquire."];
      lines.push("Name: " + data.name);
      if (data.program) lines.push("Program: " + data.program);
      lines.push("Phone: " + data.phone);
      if (data.email) lines.push("Email: " + data.email);
      if (data.message) lines.push("Message: " + data.message);
      return lines.join("\n");
    }
    function setLoading(on) {
      if (!btn) return;
      if (on) { btn.setAttribute("data-loading", ""); btn.setAttribute("aria-busy", "true"); if (btnLabel) btnLabel.textContent = "Sending"; }
      else { btn.removeAttribute("data-loading"); btn.removeAttribute("aria-busy"); if (btnLabel) btnLabel.textContent = idleText; }
    }
    function show(state) {
      form.hidden = true;
      if (state) { state.classList.add("is-on"); state.setAttribute("tabindex", "-1"); state.focus(); }
    }

    form.addEventListener("submit", function (e) {
      e.preventDefault();
      if (alertBox) alertBox.classList.remove("is-on");
      var fields = form.querySelectorAll("input, select, textarea");
      var ok = true, firstBad = null;
      fields.forEach(function (f) { if (f.name === "company") return; if (!validate(f)) { ok = false; firstBad = firstBad || f; } });
      if (!ok) {
        if (alertBox) { alertBox.textContent = "Check the highlighted fields and try again."; alertBox.classList.add("is-on"); }
        if (firstBad) firstBad.focus();
        return;
      }
      var hp = form.querySelector("[name=company]"); if (hp && hp.value) return; // spam trap

      var data = {};
      fields.forEach(function (f) { if (f.name && f.name !== "company") data[f.name] = f.value.trim(); });
      data.page = form.getAttribute("data-enquiry");
      setLoading(true);

      var wa = "https://wa.me/" + CONFIG.WHATSAPP_NUMBER + "?text=" + encodeURIComponent(composeText(data));
      if (okState) { var waBtn = okState.querySelector("[data-wa]"); if (waBtn) waBtn.href = wa; }
      if (errState) { var waErr = errState.querySelector("[data-wa]"); if (waErr) waErr.href = wa; }

      if (!CONFIG.FORM_ENDPOINT) {
        // No backend connected: prepare the message and hand over to WhatsApp / phone
        setTimeout(function () { setLoading(false); show(okState); }, 700);
        return;
      }
      fetch(CONFIG.FORM_ENDPOINT, {
        method: "POST",
        headers: { "Content-Type": "application/json", "Accept": "application/json" },
        body: JSON.stringify(data)
      }).then(function (r) {
        setLoading(false);
        if (!r.ok) throw new Error("HTTP " + r.status);
        if (okState) { okState.classList.add("is-sent"); }
        show(okState);
      }).catch(function () {
        setLoading(false);
        show(errState);
      });
    });

    // "Edit enquiry" / "Try again" buttons
    if (wrap) wrap.querySelectorAll("[data-form-back]").forEach(function (b) {
      b.addEventListener("click", function () {
        [okState, errState].forEach(function (s) { if (s) s.classList.remove("is-on"); });
        form.hidden = false;
        var f = form.querySelector("input, select, textarea"); if (f) f.focus();
      });
    });
  });

  /* ---------- Year ---------- */
  document.querySelectorAll("[data-year]").forEach(function (el) { el.textContent = new Date().getFullYear(); });
})();
