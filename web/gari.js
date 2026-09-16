const $ = (id) => document.getElementById(id);
let currentGraph = null;

const TYPE_ORDER = [
  'ResearchProgram','Source','CanonNode','Framework','ResearchQuestion','Hypothesis','Claim','Model','Dataset',
  'Simulation','Experiment','Benchmark','TelemetryObservation','Evidence','BranchFinding','Synthesis','Decision',
  'ResearchPacket','SoftwareSpecification','Publication','CaseStudy','Correction','Supersession','ProofReceipt'
];
const EVIDENCE_ORDER = ['E0_CANONICAL','E1_OPERATIONAL','E2_FORMAL','E3_EXECUTABLE','E4_PREDICTIVE','E5_DISCRIMINATIVE','E6_REPLICATED','E7_INDEPENDENT'];

async function loadRuntime() {
  try {
    const res = await fetch('/ready');
    const data = await res.json();
    $('runtime').textContent = `CORE ${data.core.toUpperCase()} · GARI CASEGRAPH ${String(data.gari_casegraph_universal || 'unknown').toUpperCase()}`;
    $('runtime').classList.add('ok');
  } catch (_) {
    $('runtime').textContent = 'RUNTIME UNAVAILABLE';
    $('runtime').classList.add('bad');
  }
}

async function loadDemo() {
  const res = await fetch('/gari/research-graph/demo');
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  setGraph(await res.json());
}

async function buildResearchGraph() {
  let payload;
  try {
    payload = JSON.parse($('research-json').value);
  } catch (error) {
    alert(`Invalid JSON: ${error}`);
    return;
  }
  const res = await fetch('/gari/research-graph', {
    method: 'POST',
    headers: {'content-type': 'application/json'},
    body: JSON.stringify(payload)
  });
  if (!res.ok) {
    const detail = await res.text();
    throw new Error(`HTTP ${res.status}: ${detail}`);
  }
  setGraph(await res.json());
}

function setGraph(graph) {
  currentGraph = graph;
  $('graph-title').textContent = graph.title;
  $('graph-id').textContent = graph.graph_id;
  populateFilters(graph);
  render();
}

function populateFilters(graph) {
  const dimensions = [
    ['type-filter', [...new Set(graph.nodes.map(n => n.object_type))].sort(sortTypes)],
    ['branch-filter', [...new Set(graph.nodes.map(n => n.branch).filter(Boolean))].sort()],
    ['evidence-filter', [...new Set(graph.nodes.map(n => n.evidence_state).filter(Boolean))].sort((a,b) => EVIDENCE_ORDER.indexOf(a) - EVIDENCE_ORDER.indexOf(b))],
    ['status-filter', [...new Set(graph.nodes.map(n => n.status).filter(Boolean))].sort()]
  ];
  dimensions.forEach(([id, values]) => {
    const select = $(id);
    const previous = select.value;
    select.innerHTML = '<option value="">ALL</option>' + values.map(v => `<option value="${escapeAttr(v)}">${escapeHtml(v)}</option>`).join('');
    if (values.includes(previous)) select.value = previous;
  });
}

function filteredNodes() {
  if (!currentGraph) return [];
  const type = $('type-filter').value;
  const branch = $('branch-filter').value;
  const evidence = $('evidence-filter').value;
  const status = $('status-filter').value;
  return currentGraph.nodes.filter(node =>
    (!type || node.object_type === type) &&
    (!branch || node.branch === branch) &&
    (!evidence || node.evidence_state === evidence) &&
    (!status || node.status === status)
  );
}

function render() {
  if (!currentGraph) return;
  const nodes = filteredNodes();
  const ids = new Set(nodes.map(node => node.id));
  const edges = currentGraph.edges.filter(edge => ids.has(edge.source) && ids.has(edge.target));
  renderSummary(nodes, edges);
  renderGraph(nodes, edges);
  renderEvidence(nodes);
  renderState(nodes);
  renderEdges(edges);
  renderReceipt(nodes, edges);
}

function renderSummary(nodes, edges) {
  const contradictions = edges.filter(e => e.relation === 'CONTRADICTS').length;
  const proofs = nodes.filter(n => n.object_type === 'ProofReceipt').length;
  const unresolved = nodes.filter(n => ['UNRESOLVED','UNKNOWN','BLOCKED'].includes(String(n.status).toUpperCase())).length;
  $('summary').innerHTML = [
    ['OBJECTS', nodes.length], ['RELATIONS', edges.length], ['CONTRADICTIONS', contradictions], ['PROOF RECEIPTS', proofs], ['UNRESOLVED', unresolved]
  ].map(([label,value]) => `<div><strong>${value}</strong><span>${label}</span></div>`).join('');
}

function renderGraph(nodes, edges) {
  const svg = $('research-graph');
  const empty = $('graph-empty');
  if (!nodes.length) {
    svg.innerHTML = '';
    empty.style.display = 'grid';
    return;
  }
  empty.style.display = 'none';
  const groups = [...new Set(nodes.map(n => n.object_type))].sort(sortTypes);
  const colWidth = 245;
  const rowHeight = 104;
  const nodeWidth = 205;
  const nodeHeight = 72;
  const marginX = 36;
  const marginY = 42;
  const position = new Map();
  let maxRows = 1;

  groups.forEach((group, col) => {
    const groupNodes = nodes.filter(n => n.object_type === group);
    maxRows = Math.max(maxRows, groupNodes.length);
    groupNodes.forEach((node, row) => {
      position.set(node.id, {x: marginX + col * colWidth, y: marginY + row * rowHeight});
    });
  });

  const width = Math.max(900, marginX * 2 + groups.length * colWidth);
  const height = Math.max(420, marginY * 2 + maxRows * rowHeight);
  svg.setAttribute('viewBox', `0 0 ${width} ${height}`);
  svg.setAttribute('width', width);
  svg.setAttribute('height', height);

  const edgeMarkup = edges.map(edge => {
    const a = position.get(edge.source);
    const b = position.get(edge.target);
    if (!a || !b) return '';
    const x1 = a.x + nodeWidth;
    const y1 = a.y + nodeHeight / 2;
    const x2 = b.x;
    const y2 = b.y + nodeHeight / 2;
    const cx = (x1 + x2) / 2;
    const path = `M ${x1} ${y1} C ${cx} ${y1}, ${cx} ${y2}, ${x2} ${y2}`;
    return `<g class="research-edge"><path d="${path}"/><text x="${cx}" y="${(y1+y2)/2 - 5}">${escapeHtml(edge.relation)}</text></g>`;
  }).join('');

  const nodeMarkup = nodes.map(node => {
    const p = position.get(node.id);
    const evidence = node.evidence_state || 'NO_EVIDENCE_STATE';
    const label = truncate(node.canonical_name, 27);
    const branch = truncate(node.branch || node.owner || 'UNASSIGNED', 26);
    return `<g class="research-node" data-id="${escapeAttr(node.id)}" transform="translate(${p.x},${p.y})" tabindex="0" role="button">
      <rect width="${nodeWidth}" height="${nodeHeight}" rx="12"/>
      <text class="node-type" x="12" y="18">${escapeHtml(node.object_type)}</text>
      <text class="node-label" x="12" y="40">${escapeHtml(label)}</text>
      <text class="node-meta" x="12" y="59">${escapeHtml(evidence)} · ${escapeHtml(branch)}</text>
    </g>`;
  }).join('');

  svg.innerHTML = `<defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z"/></marker></defs>${edgeMarkup}${nodeMarkup}`;
  svg.querySelectorAll('.research-node').forEach(el => {
    const select = () => showNode(currentGraph.nodes.find(n => n.id === el.dataset.id));
    el.addEventListener('click', select);
    el.addEventListener('keydown', event => { if (event.key === 'Enter' || event.key === ' ') select(); });
  });
}

function renderEvidence(nodes) {
  const counts = Object.fromEntries(EVIDENCE_ORDER.map(e => [e, 0]));
  nodes.forEach(node => { if (node.evidence_state) counts[node.evidence_state] = (counts[node.evidence_state] || 0) + 1; });
  const max = Math.max(1, ...Object.values(counts));
  $('evidence-ladder').innerHTML = EVIDENCE_ORDER.map(state => {
    const value = counts[state] || 0;
    const pct = Math.round(value / max * 100);
    return `<div class="ladder-row"><span>${state}</span><div><i style="width:${pct}%"></i></div><b>${value}</b></div>`;
  }).join('');
}

function renderState(nodes) {
  const branches = countBy(nodes.map(n => n.branch).filter(Boolean));
  const statuses = countBy(nodes.map(n => n.status).filter(Boolean));
  const owners = countBy(nodes.map(n => n.owner).filter(Boolean));
  $('research-state').innerHTML = [
    ['BRANCHES', branches], ['STATUSES', statuses], ['OWNERS', owners]
  ].map(([title, values]) => `<section><h3>${title}</h3>${Object.entries(values).sort((a,b) => b[1]-a[1]).map(([k,v]) => `<div><span>${escapeHtml(k)}</span><b>${v}</b></div>`).join('') || '<em>None</em>'}</section>`).join('');
}

function renderEdges(edges) {
  $('edge-ledger').innerHTML = edges.length ? edges.map(edge => {
    const source = currentGraph.nodes.find(n => n.id === edge.source);
    const target = currentGraph.nodes.find(n => n.id === edge.target);
    return `<div class="edge-row"><span>${escapeHtml(source?.canonical_name || edge.source)}</span><b>${escapeHtml(edge.relation)}</b><span>${escapeHtml(target?.canonical_name || edge.target)}</span></div>`;
  }).join('') : '<div class="muted">No visible relations under the current filters.</div>';
}

function renderReceipt(nodes, edges) {
  $('graph-receipt').textContent = JSON.stringify({
    contract: currentGraph.contract,
    provider: currentGraph.provider,
    graph_id: currentGraph.graph_id,
    program_id: currentGraph.program_id,
    visible_objects: nodes.length,
    visible_relations: edges.length,
    full_summary: currentGraph.summary,
    generated_at: currentGraph.generated_at,
    truth_boundary: currentGraph.truth_boundary
  }, null, 2);
}

function showNode(node) {
  if (!node) return;
  $('selected-object').innerHTML = `
    <h3>${escapeHtml(node.canonical_name)}</h3>
    <div class="object-tags"><span>${escapeHtml(node.object_type)}</span>${node.evidence_state ? `<span>${escapeHtml(node.evidence_state)}</span>` : ''}<span>${escapeHtml(node.status)}</span></div>
    ${node.description ? `<p>${escapeHtml(node.description)}</p>` : ''}
    <dl>${detailRows(node)}</dl>
    ${node.payload && Object.keys(node.payload).length ? `<pre>${escapeHtml(JSON.stringify(node.payload, null, 2))}</pre>` : ''}`;
}

function detailRows(node) {
  const fields = [
    ['ID', node.id], ['BRANCH', node.branch], ['PROGRAM', node.program_id], ['OWNER', node.owner], ['VERSION', node.version],
    ['DEPLOYMENT', node.deployment_status], ['EVIDENCE GRADE', node.evidence_grade], ['ACCESS', node.access_class],
    ['SOURCES', (node.source_refs || []).join('\n')], ['PROVENANCE', (node.provenance || []).join('\n')], ['PROOFS', (node.proof_refs || []).join('\n')],
    ['DEPENDENCIES', (node.dependencies || []).join('\n')], ['RELATED', (node.related_objects || []).join('\n')], ['CREATED', node.created_at], ['UPDATED', node.updated_at]
  ];
  return fields.filter(([,v]) => v).map(([k,v]) => `<div><dt>${k}</dt><dd>${escapeHtml(String(v)).replaceAll('\n','<br>')}</dd></div>`).join('');
}

function countBy(values) {
  return values.reduce((acc, value) => { acc[value] = (acc[value] || 0) + 1; return acc; }, {});
}
function sortTypes(a,b) {
  const ai = TYPE_ORDER.indexOf(a); const bi = TYPE_ORDER.indexOf(b);
  return (ai < 0 ? 999 : ai) - (bi < 0 ? 999 : bi) || a.localeCompare(b);
}
function truncate(value, n) { return value.length > n ? `${value.slice(0,n-1)}…` : value; }
function escapeHtml(value) { const d = document.createElement('div'); d.textContent = String(value ?? ''); return d.innerHTML; }
function escapeAttr(value) { return escapeHtml(value).replaceAll('"','&quot;'); }

$('demo').addEventListener('click', () => loadDemo().catch(err => alert(String(err))));
$('toggle-import').addEventListener('click', () => $('import-wrap').classList.toggle('hidden'));
$('build-research').addEventListener('click', () => buildResearchGraph().catch(err => alert(String(err))));
['type-filter','branch-filter','evidence-filter','status-filter'].forEach(id => $(id).addEventListener('change', render));

loadRuntime();
loadDemo().catch(() => {});
