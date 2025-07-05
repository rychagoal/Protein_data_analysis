function fetchAnswer(url, elementId) {
    fetch(url)
        .then(response => response.json())
        .then(data => {
            const el = document.getElementById(elementId);
            el.innerHTML = formatAnswer(data);
        });
}

function formatAnswer(data) {
    if (data.answer !== undefined) {
        return `<p><strong>${data.answer}</strong></p>`;
    }
    if (data.mean !== undefined && data.std !== undefined) {
        return `<p><strong>Mean:</strong> ${data.mean}, <strong>Std:</strong> ${data.std}</p>`;
    }
    if (data.domain !== undefined) {
        return `<p><strong>Domain:</strong> ${data.domain}, <strong>Average abundance:</strong> ${data.avg_abundance}, <strong>Times seen:</strong> ${data.times_seen}</p>`;
    }
    if (data.table !== undefined) {
        const keys = Object.keys(data.table[0]);
        let table = '<table border="1"><thead><tr>';
        keys.forEach(key => table += `<th>${key}</th>`);
        table += '</tr></thead><tbody>';
        data.table.forEach(row => {
            table += '<tr>';
            keys.forEach(key => table += `<td>${row[key]}</td>`);
            table += '</tr>';
        });
        table += '</tbody></table>';
        return table;
    }
    return `<p>No data returned.</p>`;
}