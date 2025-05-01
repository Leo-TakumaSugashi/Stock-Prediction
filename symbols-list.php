<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CSV Sortable Table</title>
    <script>
        let csvData = <?php
            $data = [];
            if (($handle = fopen('Symbol_List_Info.csv', 'r')) !== false) {
                $header = fgetcsv($handle);
                while (($row = fgetcsv($handle)) !== false) {
                    $data[] = array_combine($header, $row);
                }
                fclose($handle);
            }
            echo json_encode($data, JSON_UNESCAPED_UNICODE);
        ?>;
    </script>
    <style>
        th {
            cursor: pointer;
        }
    </style>
</head>
<body>
<h1><?php echo "List of Symbols - " . date("Y/m/d (l)")  ?></h1>
<h3>Click on header to sort. </h3>
<table id="csvTable" border="1">
    <thead>
        <tr>
            <th>Index</th>
            <th onclick="sortTable('Symbol', this)">Symbol(=)</th>
            <th onclick="sortTable('Name', this)">Name(=)</th>
            <th onclick="sortTable('Markert', this)">Market(=)</th>
            <th onclick="sortTable('Sector', this)">Sector(=)</th>
            <th onclick="sortTable('FullName', this)">FullName(=)</th>
        </tr>
    </thead>
    <tbody>
        <!-- JavaScriptでテーブルデータを埋め込む -->
    </tbody>
</table>
<p class="poweredby" style="float: right;font-size:9px">powered by Yahoo Finance (yfinance api on python).</p>
<script>
    // テーブルのデータを表示する関数
    function renderTable(data) {
        const tbody = document.querySelector("#csvTable tbody");
        tbody.innerHTML = "";  // テーブルの内容をクリア
        data.forEach(row => {
            const tr = document.createElement('tr');
            for (const key in row) {
                const td = document.createElement('td');
                td.textContent = row[key];
                tr.appendChild(td);
            }
            tbody.appendChild(tr);
        });
    }

    // 初期データの描画
    renderTable(csvData);

    // 昇順・降順をトグルするフラグ
    let sortOrder = true;

    // テーブルをソートする関数
    function sortTable(column, headerElement) {
        // ヘッダーの全列のソート状態をリセット
        const headers = document.querySelectorAll("th");
        headers.forEach(th => {
            th.textContent = th.textContent.replace(/[\u2191\u2193]/g, "(=)");
        });

        // ソートの方向に応じて矢印をセット
        if (sortOrder) {
            headerElement.textContent = headerElement.textContent.replace("(=)", "\u2191");  // 昇順↑
        } else {
            headerElement.textContent = headerElement.textContent.replace("(=)", "\u2193");  // 降順↓
        }

        // データをソート
        csvData.sort((a, b) => {
            let aVal = a[column].toLowerCase();
            let bVal = b[column].toLowerCase();

            if (aVal < bVal) return sortOrder ? -1 : 1;
            if (aVal > bVal) return sortOrder ? 1 : -1;
            return 0;
        });

        // 次回クリック時のソート順を反転
        sortOrder = !sortOrder;

        // ソート後に再描画
        renderTable(csvData);
    }
</script>

</body>
</html>
