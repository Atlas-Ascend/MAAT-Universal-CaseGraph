const $ = (id) => document.getElementById(id);

async function loadRuntime() {
  try {
    const res = await fetch('/ready');
    const data = await res.json();
    $('runtime').textContent = `CORE ${data.core.toUpperCase()} · AGENT ${data.agent_runtime.toUpperCase()}`;
    $('runtime').classList.add('ok');
  } catch (_) {
    $('runtime').textContent = 'RUNTIME UNAVAILABLE';
    $('runtime').classList.add('bad');
  }
}

$('build').addEventListener('click', async () => {
  $('build').disabled = true;
  $('build').textContent = 'BUILDING CASE…';
  $('graph').textContent = 'Constructing typed graph…';
  $('findings').textContent = 'Running evidence and dependency reasoning…';
  $('receipt').textContent = 'Awaiting verified receipt…';

  try {
    const res = await fetch('/build-case', {
      method: 'POST',
      headers: {'content-type': 'application/json'},
      body: JSON.stringify({text: $('input').value})
    });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = await res.json();

    $('run-id').textContent = data.meta.run_id;
    $('pipeline').textContent = data.meta.pipeline.join(' → ');
    $('summary').innerHTML = [
      ['NODES', data.meta.counts.nodes],
      ['EDGES', data.meta.counts.edges],
      ['FINDINGS', data.meta.counts.findings],
      ['ACTIONS', data.meta.counts.actions]
    ].map(([label, value]) => `<div><strong>${value}</strong><span>${label}</span></div>`).join('');

    $('graph').innerHTML = data.graph.nodes.map((node) =>
      `<span class="node"><b>${escapeHtml(node.type.toUpperCase())}</b>${escapeHtml(node.label)}</span>`
    ).join('');

    $('findings').innerHTML = data.graph.findings.length
      ? data.graph.findings.map((finding) => `<div class="finding"><b>${escapeHtml(finding.kind.toUpperCase())}</b><span>${escapeHtml(finding.summary)}</span></div>`).join('')
      : '<div class="finding"><b>CLEAR</b><span>No explicit blocker or evidence gap detected.</span></div>';

    $('receipt').textContent = JSON.stringify(data.receipt, null, 2);
  } catch (err) {
    $('graph').textContent = 'Case build failed.';
    $('findings').textContent = String(err);
    $('receipt').textContent = 'No PASS receipt emitted.';
  } finally {
    $('build').disabled = false;
    $('build').textContent = 'BUILD CASE';
  }
});

function escapeHtml(value) {
  const div = document.createElement('div');
  div.textContent = value;
  return div.innerHTML;
}

loadRuntime();
