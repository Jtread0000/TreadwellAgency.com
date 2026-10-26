/* Treadwell Agency — mobile nav toggle */
(function () {
  var burger = document.querySelector('.burger');
  var menu = document.getElementById('mobile-menu');
  if (!burger || !menu) return;
  burger.addEventListener('click', function () {
    var open = menu.classList.toggle('open');
    burger.setAttribute('aria-expanded', open ? 'true' : 'false');
  });
})();

// Newsletter capture: posts to the shared Treadwell capture layer, which stores the signup
// and syncs it to Kit tagged brand:agency.
(function () {
  var forms = document.querySelectorAll('form.nl-form');
  Array.prototype.forEach.call(forms, function (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var msg = form.querySelector('.nl-msg');
      var email = (form.email.value || '').trim();
      if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)) { msg.textContent = 'Enter an email address.'; return; }
      var btn = form.querySelector('button'); btn.disabled = true; msg.textContent = 'Adding you…';
      fetch('https://joinpromptschool.com/api/subscribe', {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email: email, firstName: (form.firstName.value || '').trim(), brand: 'agency', source: form.getAttribute('data-source') || 'treadwellagency.com', website: form.website.value || '' })
      }).then(function (r) { return r.ok ? r.json() : Promise.reject(r); })
        .then(function () { form.innerHTML = '<p style="margin:0;font-weight:700;color:#000;">You are on the list. One email when something moves.</p>'; })
        .catch(function () { btn.disabled = false; msg.textContent = 'That did not go through. Try again, or email hello@treadwellagency.com.'; });
    });
  });
})();
