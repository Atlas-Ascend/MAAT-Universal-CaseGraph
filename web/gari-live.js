async function loadCanonicalGari() {
  const button = document.getElementById('canonical');
  if (button) {
    button.disabled = true;
    button.textContent = 'LOADING GARI…';
  }
  try {
    const response = await fetch('/gari/research-graph/canonical', {cache: 'no-store'});
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const graph = await response.json();
    setGraph(graph);
    if (button) button.textContent = 'REFRESH LIVE GARI';
  } catch (error) {
    console.error('Canonical GARI load failed', error);
    if (button) button.textContent = 'RETRY LIVE GARI';
  } finally {
    if (button) button.disabled = false;
  }
}

const canonicalButton = document.getElementById('canonical');
if (canonicalButton) canonicalButton.addEventListener('click', loadCanonicalGari);

// gari.js still preserves the bounded Brain Cycle demo. The canonical Institute
// snapshot intentionally loads after that bootstrap so the production surface
// settles on the live research map rather than the demonstration fixture.
window.setTimeout(loadCanonicalGari, 750);
