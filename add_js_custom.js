document.addEventListener('DOMContentLoaded', function () {
    const addRowButton = document.getElementById('add-row');

    addRowButton.addEventListener('click', function () {
        const table = document.getElementById('items-table').getElementsByTagName('tbody')[0];
        const rowCount = table.rows.length;
        const newRow = table.insertRow(rowCount);

        // 定義列名及其 data-label
        const columns = [
            { name: 'no', label: 'NO' },
            { name: 'item', label: '品項' },
            { name: 'quantity', label: '數量' },
            { name: 'price', label: '價格/元' },
            { name: 'remark', label: '備註' },
        ];

        // 動態生成列
        columns.forEach((col, index) => {
            const cell = newRow.insertCell(index);
            cell.setAttribute('data-label', col.label); // 設置 data-label
            const input = document.createElement('input');
            input.type = 'text';
            input.name = `items[${rowCount}][${col.name}]`;
            input.value = '';
            cell.appendChild(input);
        });

        // 添加操作按钮
        const actionCell = newRow.insertCell(columns.length);
        actionCell.setAttribute('data-label', '操作'); // 設置操作列的 data-label
        const deleteButton = document.createElement('button');
        deleteButton.type = 'button';
        deleteButton.className = 'delete-row';
        deleteButton.textContent = '刪除';
        deleteButton.addEventListener('click', function () {
            newRow.remove();
        });
        actionCell.appendChild(deleteButton);

        // 綁定刪除事件
        deleteButton.addEventListener('click', function () {
            table.deleteRow(newRow.rowIndex - 1);
        });
    });

    // 綁定刪除按鈕的初始行
    document.querySelectorAll('.delete-row').forEach(function (button) {
        button.addEventListener('click', function () {
            const row = button.closest('tr');
            row.parentNode.removeChild(row);
        });
    });
});

document.getElementById('submit-form').addEventListener('click', function () {
    const formData = new FormData(document.getElementById('custom-form'));
    const formattedData = {
        client_info: {
            name: formData.get('name'),
            phone: formData.get('phone'),
            date: formData.get('date'),
            lead_time: formData.get('lead_time'),
            location: formData.get('location'),
            sales: formData.get('sales'),
        },
        price: {
            discount: formData.get('discount'),
            gift: formData.get('gift'),
        },
        items: [],
    };
	
// 處理商品明細
    const itemsTable = document.getElementById('items-table').getElementsByTagName('tbody')[0];
    Array.from(itemsTable.rows).forEach((row, index) => {
        const itemData = {
            no: row.querySelector(`input[name="items[${index}][no]"]`).value,
            item: row.querySelector(`input[name="items[${index}][item]"]`).value,
            quantity: row.querySelector(`input[name="items[${index}][quantity]"]`).value,
            price: row.querySelector(`input[name="items[${index}][price]"]`).value,
            remark: row.querySelector(`input[name="items[${index}][remark]"]`).value,
        };
        formattedData.items.push(itemData);
    });

    // 發送請求並處理回應
    fetch('https://alohamico.com:8000/generate-invoice/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(formattedData),
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('PDF 生成失敗');
            }
            return response.blob();
        })
        .then(blob => {
        const url = window.URL.createObjectURL(blob);

        const a = document.createElement('a');
            if ('download' in a) {
                // 如果支持 download 属性，触发下载
                a.style.display = 'none';
                a.href = url;
                a.download = 'invoice.pdf'; // 下载的文件名
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
            } else {
                // 如果不支持 download 属性，直接打开文件
                window.open(url, '_blank');
            }
        window.URL.revokeObjectURL(url);
    })
    .catch(error => {
        console.error('錯誤：', error);
        alert('提交失敗，請檢查控制台的錯誤訊息。');
    });
});