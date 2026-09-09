const $ = (id) => document.getElementById(id);

$('build').addEventListener('click', async () => {
  $('graph').textContent = 'Constructing case…';
  $('receipt').textContent = 'Awaiting receipt…';
  try {
    const res = await fetch('/build-case', {
      method: 'POST',
      headers: {'content-type': 'application/json'},
      body: JSON.stringify({text: $('input').value})
    });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = await res.json();
    $('graph').innerHTML = data.graph.nodes.map(n => `<span class="node">${n.type.toUpperCase()} · ${escapeHtml(n.label)}</span>`).join('');
    $('receipt').textContent = JSON.stringify(data.receipt, null, 2);
  } catch (err) {
    $('graph').textContent = 'API not connected. Run the FastAPI service and serve this UI from the same origin.';
    $('receipt').textContent = String(err);
  }
});

function escapeHtml(value) {
  const div = document.createElement('div');
  div.textContent = value;
  return div.innerHTML;
}
