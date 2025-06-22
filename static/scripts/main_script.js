function fetchAnswer(qid, elid) {
    fetch('/api/' + qid)
      .then(resp => resp.json())
      .then(data => {
        let el = document.getElementById(elid);
        if (data.error) {
            el.innerHTML = `<span class="error">${data.error}</span>`;
            return;
        }
        // A1
        if (["A1-1", "A1-2", "A1-3"].includes(qid)) {
            el.innerHTML = `<b>${data.answer}</b>`;
        }
        // A2-1
        else if (qid === "A2-1") {
            el.innerHTML = `<b>${data.mean}</b>, <b>${data.std}</b>`;
        }
        // A2-2
        else if (qid === "A2-2") {
            if (!data.table || data.table.length === 0) { el.innerHTML = "No data"; return; }
            let rows = data.table.map(r =>
                `<tr>
                    <td>${r.Gn}</td>
                    <td>${typeof r.mean === 'number' ? r.mean.toFixed(2) : '-'}</td>
                    <td>${typeof r.std === 'number' ? r.std.toFixed(2) : '-'}</td>
                </tr>`
            ).join('');
            el.innerHTML = `<table>
                <tr><th>Protein (Gn)</th><th>Mean</th><th>Std</th></tr>
                ${rows}
            </table>`;
        }
        // A3
        else if (qid === "A3") {
            if (!data.table || data.table.length === 0) { el.innerHTML = "No data"; return; }
            let rows = data.table.map(r =>
                `<tr>
                    <td>${r.Gn}</td>
                    <td>${typeof r.mean === 'number' ? r.mean.toFixed(2) : '-'}</td>
                    <td>${typeof r.std === 'number' ? r.std.toFixed(2) : '-'}</td>
                    <td>${typeof r.percentile_rank === 'number' ? r.percentile_rank.toFixed(3) : '-'}</td>
                </tr>`
            ).join('');
            el.innerHTML = `<table>
                <tr><th>Protein (Gn)</th><th>Mean</th><th>Std</th><th>Percentile rank</th></tr>
                ${rows}
            </table>`;
        }
        // B1
        else if (qid === "B1") {
            el.innerHTML = `
                <div><b>${data.domain}</b></div>
                <div><b>${data.avg_abundance}</b></div>
                <div><b>${data.times_seen}</b></div>
            `;
        }
        // B2
        else if (qid === "B2") {
            if (!data.table || data.table.length === 0) { el.innerHTML = "No data"; return; }
            let rows = data.table.map(r =>
                `<tr>
                    <td>${r.Domain}</td>
                    <td>${typeof r.domain_average_abundance === 'number' ? r.domain_average_abundance : '-'}</td>
                    <td>${typeof r.domain_abundance_std === 'number' ? r.domain_abundance_std : '-'}</td>
                    <td>${typeof r.count_domain === 'number' ? r.count_domain : '-'}</td>
                    <td>${typeof r.percentile_rank === 'number' ? r.percentile_rank.toFixed(2) : '-'}</td>
                </tr>`
            ).join('');
            el.innerHTML = `<table>
                <tr>
                    <th>Domain</th>
                    <th>Mean abundance</th>
                    <th>Std</th>
                    <th>Count</th>
                    <th>Percentile</th>
                </tr>
                ${rows}
            </table>`;
        }
      });
}