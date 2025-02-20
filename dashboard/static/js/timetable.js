document.getElementById('addRow').addEventListener('click', function() {
    const table = document.getElementById('day-schedule');
    const newRow = table.rows[0].cloneNode(true);
    newRow.querySelectorAll('input, select').forEach(input => input.value = '');
    table.appendChild(newRow);
  });
  
  document.getElementById('day-schedule').addEventListener('click', function(e) {
    if (e.target.classList.contains('delete-row')) {
      e.target.closest('tr').remove();
    }
  });
  