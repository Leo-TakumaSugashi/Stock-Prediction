<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Result Check[:D]</title>
    <style>
        /* テキストの自動サイズ調整を無効化し、任意のサイズを指定 */
        body {
            -webkit-text-size-adjust: 100%; 
            font-size: 20px; 
        }
        .headers {
            position:fixed;
            top:0%;
            height:90px;
            background:rgba(255,255,255,0.95);
            width:100%;
            z-index: 10;
        }
        .headers p {
            padding-right: 30px;
            padding-top:40px;
            float:right;
            font-size: 16px;
            font-style: italic;
        }
        .tablelink {
            color:white; 
            background:rgba(0,0,0,0.99); 
            position:fixed;
            top:90px;
            font-family:"Comic Sans MS, cursive";
            font-size: 24pt;
            text-align:center;
            height:28pt;
            width:100%;
            z-index: 10;
        }
        .tablelink a{
            color:rgb(60,255,255);
            padding:10pt 50pt 10pt 0;
        }
        .timezones {
            text-align:left;
            padding-left:20%;
            padding-right:20%;
            /* min-width: 800px; */
            font-family:"Brush Script MT, cursive";
            font-size:14pt;
        }
        .timezones p { 
            line-height: 9px;
            text-align: left;
        }
        .marquee {
            width: 100%;
            white-space: nowrap;
            overflow: hidden;
            box-sizing: border-box;
            background-color: #f0f0f0;
            padding: 10px 0;
        }
        .marquee span {
            display: inline-block;
            padding-left: 50%;
            animation: marquee 20s linear infinite; /* アニメーション速度を調整 */
            font-family: 'Courier New', Courier, monospace;
            font-size: 18px;
            font-style: italic;
            font-stretch: narrower;
            font-weight: bold;
            color: rgb(0, 0, 140);
        }

        @keyframes marquee {
            0% {
                transform: translateX(100%);
            }
            100% {
                transform: translateX(-100%);
            }
        }

        .gallery {
            /* float: both; */
            /* grid-template-columns: repeat(3, 1fr); */
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            width: 100%;
        }
        .gallery img {
            width: calc(33.33% - 10px);;
            height: auto;
        }
        .classification {
            margin:  0;
            position: relative;
        }
        #image-container {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 0;
            -webkit-text-size-adjust: 100%;
            font-size: 30px;
        }
        .landscape {
            grid-column: span 2; /* 横長の画像は2列分を使用 */
        }

        .portrait {
            grid-column: span 1; /* 縦長の画像は通常の1列分を使用 */
        }
        .img {
            position: absolute;
            left: -100px;
            min-width: 120%;
            min-height: 120%;
        }
        .controls {
            position: fixed;
            display: none;
            bottom: 0;
            left: 0;
            margin: 0 0 10px 0;
            width: 100%;
            height: 52px;
            background-color: rgba(0,0,0,0.7);
            vertical-align: middle;
        }
        .inputers {
            font-size:16pt;
            background-image:url('login/modify/sigmoid_gaussian.png');
            background-repeat:no-repeat;
            background-size:cover;
            background-position-x:-40px;
            background-position-y:-10px;
            background-color:rgba(255,255,255,0.7);
            background-blend-mode:lighten;
            width:100%;
            color:rgb(0,0,0);
        }
        .inputers label, button, select, input{font-size: 16pt; line-height:32pt;}
        .inputers button, select {
            -webkit-text-size-adjust: 100%;
            font-size: 18px;
            max-width: 33.3%;
        }
        .inputers button {margin-left:10%; margin-top:20px;}
        /* button#classify-all-button { */
            /* font-size: 30px; */
            /* margin-left: 20px; */
            /* background-color: aqua; */
        /* } */
        /* label { */
            /* font-size: 25px; */
            /* font-family: 'Times New Roman', Times, serif; */
        /* } */
        .imglabel {
            font-size: 18px;
            margin-left: 10%;
            text-align: center;
        }
        .mycomments {
            margin: 0;
            padding: 5px;
            font-style:italic;
            font-size: 16pt;
        }
        .mycomments p {
            margin: 0;
            padding: 0;
        }
        /* p { line-height: 12px} */
        @media screen and (max-width: 1050px) {
            .headers p {
                padding-right: 10pt;
                padding-top: 0;
            }
            .headers h1 { line-height: 9px; }
            .tablelink { font-size:12pt; height:16pt;}
            .tablelink a{ padding-right: 10pt}
            .timezones {
                font-size:10pt;
                padding-left:10pt;
                padding-right:10pt;
            }
            .timezones p { 
                line-height: 9px;
                font-size:9pt;
            }
            .mycomments {
                padding:1pt;
                font-size:10pt;
            }
            .marquee span { font-size:10pt; }
            h1 {
                font-size: 25px;
            }
            .inputers {font-size: 11pt; }
            .inputers label, button, select, input{font-size: 11pt; line-height:24pt;}
            #image-container {
                grid-template-columns: repeat(2, 1fr);
                gap: 1px;
            }
            .controls {
                bottom: 2%;
                height: 24px;
            }
            button#classify-all-button {
                float: right;
                font-size: 10px;
            }
            .controll-button {
                display: none;
            }
            .imglabel {
                font-size: 8pt;
                margin-left: 3pt;
                text-align: left;
            }
        }
    </style>
</head>
<body>
    <div class="headers">
        <h1 style="padding-left: 20px;font-style: oblique;float:left">Prediction (LSTM-Stock-Forecasting)</h1>
        <p> &copy;Leo Takuma SUGASHI.  &nbsp;&nbsp;Acknowledgments:&#x1f400;</p>
    </div>
    <div class="tablelink">
        <a href="./login/" style="color:rgb(100,255,100)"><span style="font-size:smaller">&#9654&nbsp;</span>login</a>
        <a href="./symbols-list.php" ><span style="font-size:smaller">&#9654&nbsp;</span>Symbols List</a>
        <!-- <a href="http://sugashi-rhel9.iobb.net:10110/" ><span style="font-size:smaller">&#9654&nbsp;</span>Tensor Board(latest)</a> -->
        <a href="404.php" ><span style="font-size:smaller">&#9654&nbsp;</span>Tensor Board(latest)</a>
    </div>
    <p sytle="line-height: 200px;"><br><br><br><br></p>
    <div class="marquee">
        <span id="news"></span>
    </div>
    <div class="mycomments">
        <p>９月２８日現在。Actual＆Predは過去1年分のグラフと先３０日分の予想。</p>
        <p>　モデルは毎日16時以降取得可能なデータからスクラッチ状態で計算。（Directoryの＊＊＊２ndは常に同じモデルを使用）</p>
    </div>
    <div class="timezones">
        <h3>*Today's data will be updated after 4:00 p.m. (JST)</h3>
        <p>
            <?php
            date_default_timezone_set('Europe/London');  // イギリスのタイムゾーン
            echo date("T") . "-TimeZone: " . date("l, F j, Y, g:i A") . " // London, England.";
            ?>
        </p>
        <p>
            <?php
            date_default_timezone_set('Asia/Tokyo');  // 日本標準時（JST）
            echo date("T") . "-TimeZone: " . date("l, F j, Y, g:i A") . " // Tokyo, Japan.";
            ?>
        </p>
        <p>
            <?php
            date_default_timezone_set('UTC');  
            echo date("T") . "-TimeZone: " . date("l, F j, Y, g:i A") . " // UTC";
            ?>
        </p>
    </div>
    
    <div class="inputers">
        <br><br>
        <label for="directory">Select Log-Dir. :</label>
        <select name="directory" id="directory">
        </select><br>
        <label>Figure Type : 
            <input type="checkbox" id="prediction-png" checked>
            Actual & Prediction &nbsp;&nbsp;&nbsp;
            <input type="checkbox" id="mpf-30days-png">
            Candle 30 Days
        </label><br>
        <label for="sort-type">Sort-Type :</label>
        <select name="sort-type" id="sort-type">
            <option checkd>Alphabet(ascending)</option>
            <option>Alphabet(descending)</option>
            <option>Expected increase(ascending)</option>
            <option>Expected increase(descending)</option>
        </select><br>
        <label for="num-columns">Number of Columns :</label>
        <select name="num-columns" id="num-columns">
            <option checked>Default</option>
            <option>4</option>
            <option>3</option>
            <option>2</option>
            <option>1</option>
        </select><br>

        <button onclick="displayImages()" id="showimages">Show Result</button>
    </div>
    <div id="image-title"></div>
    <div id="image-container" class="gallery">
        <!-- PHP から画像がここに挿入されます -->
    </div>
    <br><br><br><br><br><br><br><br>
    </div>
    <div class="controls">
        <button onclick="saveToJson()" style="float: right; margin: 3px; z-index: 1;">Save to JSON file.</button>
        <button onclick="setupPage()" data-pm="--" id="previous" style="margin-left: 10px;margin-bottom: 3px;">Pre.</button>
        <a id="currentindex" style="margin-left: 10px;margin-right: 10px;color: aliceblue;"><a>
        <button onclick="setupPage()" data-pm="++" id="next" style="margin: 3px;vertical-align: middle;">Next</button>
        <button id="classify-all-button">Classify All</button>
        <a id="second-title" style="margin-left: 10px;color: aliceblue;"></a>
    </div>
    
</body>
<script>
    function addOptions() {
        let currentTime = new Date();
        let checkHours = new Date();
        checkHours.setHours(16, 0, 0, 0); // Setting the time to 16:00 (4:00 PM)
        if (currentTime < checkHours) {// If the current time is less than 16:00, set the date to yesterday
            var date = new Date();
            date.setDate(date.getDate() - 1); // Go back one day
        } else { // Otherwise, set the date to today            
            var date = new Date();
        }
        let options = { timeZone: 'Asia/Tokyo', year: 'numeric', month: '2-digit', day: '2-digit', 
                    hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: false };
        let jstDate = new Intl.DateTimeFormat('ja-JP', options).format(date);
        jstDate = jstDate.replace(/\//g, "-");
        let sD = jstDate.split(" ");
        var endDate = new Date(`${sD[0]}T12:00:00+09:00`);
        var startDate = new Date('2024-09-19T12:00:00+09:00');
        var sevenDaysInMs = 7 * 24 * 60 * 60 * 1000;
        var compDate = new Date(endDate.getTime() - sevenDaysInMs)
        if (startDate < compDate) {
            startDate = compDate;
        }

        const select = document.getElementById('directory');
        var tzoffset = date.getTimezoneOffset() * 60000; //offset in milliseconds
        console.log(tzoffset)
        while (endDate >= startDate) {
            const option = document.createElement('option');
            const year = endDate.getFullYear();
            const month = ('0' + (endDate.getMonth() + 1)).slice(-2);
            const day = ('0' + endDate.getDate()).slice(-2);
            const dateStr = `${year}-${month}-${day}`; 
            option.value = dateStr;
            option.setAttribute('data-dir', 'logs/TB_logs-' + dateStr);
            option.textContent = dateStr + " ("+ getWeekday(new Date(dateStr), "en") +")";
            select.appendChild(option);
            endDate.setDate(endDate.getDate() - 1);
        };
        var endDate = new Date(`${sD[0]}T12:00:00+09:00`);
        var startDate = new Date('2024-09-24T12:00:00+09:00');
        var compDate = new Date(endDate.getTime() - sevenDaysInMs)
        if (startDate < compDate) {
            startDate = compDate;
        }
        while (endDate >= startDate) {
            const option = document.createElement('option');
            const year = endDate.getFullYear();
            const month = ('0' + (endDate.getMonth() + 1)).slice(-2);
            const day = ('0' + endDate.getDate()).slice(-2);
            const dateStr = `${year}-${month}-${day}`; 
            option.value = dateStr;
            option.setAttribute('data-dir', 'logs-keep-model/TB_logs-keep-model-' + dateStr);
            option.textContent = dateStr + " ("+ getWeekday(new Date(dateStr), "en") +") " + ':2nd ver.';
            select.appendChild(option);
            endDate.setDate(endDate.getDate() - 1);
        };
    }
    addOptions()
    const predictionCheckbox = document.getElementById('prediction-png');
    const mpfCheckbox = document.getElementById('mpf-30days-png');      

    function togglePrediction() {
        if (predictionCheckbox.checked) {
            mpfCheckbox.checked=false;
        } else {
            predictionCheckbox.checked=true;
        }
    }
    function toggleMPF30d() {
        if (mpfCheckbox.checked) {
            predictionCheckbox.checked=false;
        } else {
            mpfCheckbox.checked=true;
        }
    }
    predictionCheckbox.addEventListener('change', togglePrediction);
    mpfCheckbox.addEventListener('change', toggleMPF30d);

    let globalPageNum = 0;

    function setpopupmenu(Dir) {
        const opth = document.getElementById('directory');
        var counter = 0;
        Dir.forEach(n => {
            const option = document.createElement('option');
            option.value = `${n}`;
            option.textContent = `${n}`;
            opth.appendChild(option);
            counter++
        });
        return counter;
    }
    
    MaximumIndex = [];
    function dummy0() {
        fetch("./Symbol_List_Info.csv")
        .then((res) => res.text())
        .then((text) => {
            let splitText = text.split("\n");
            splitText.forEach((inLine, index) => {
                if (index === 0) {
                    return; // skip header
                } else {
                    let result = inLine.split(",");
                    // console.log(result[result.length - 1]); // 最後の要素を取得
                    //    MaximumIndex = setpopupmenu(splitText.slice(globalPageNum))
                }
            });
        })
        .catch((error) => console.error('Error fetching the CSV:', error));
    }
    

    function checkPageButton() {
        const dirnamehandle = document.getElementById('directory');
        var currentIndex = dirnamehandle.selectedIndex;
        const nextButton = document.getElementById('next');
        const previousButton = document.getElementById('previous')
        nextButton.style.display = 'initial';
        previousButton.style.display = 'initial';
        console.log(currentIndex.toString())
        if (currentIndex === 0) {
            previousButton.style.display = 'none';
        } else if (currentIndex === MaximumIndex) {
            nextButton.style.display = 'none';
        } else if (currentIndex === -1) {
            previousButton.style.display = 'none';
            nextButton.style.display = 'none';
        }
    }
    // checkPageButton();
    globalImagePath = []
    function displayImages() {
        const dirnamehandle = document.getElementById('directory');
        const currentIndex = dirnamehandle.selectedIndex;
        const selectedOption = dirnamehandle.options[currentIndex]; 
        const dirname = selectedOption.dataset.dir; 
        const sortTypeHandle=document.getElementById('sort-type');
        const sortType=sortTypeHandle.options[sortTypeHandle.selectedIndex].textContent;
        const numColumnsHandle = document.getElementById('num-columns');
        const numColumns = numColumnsHandle.options[numColumnsHandle.selectedIndex].textContent;
        if (numColumns !== 'Default') {
            const imageContainer = document.getElementById('image-container');
            imageContainer.style.gridTemplateColumns = `repeat(${numColumns}, 1fr)`;
        }

        var imgpath = dirname;
        if (predictionCheckbox.checked) {
            var imtype='prediction';
        } else if (mpfCheckbox.checked) {
            var imtype='mpf30days'
        }

        let sortDir;
        let sortMethod;
        if (sortType.includes('ascending')) {
            sortDir = 'ascending';
        } else {
            sortDir = 'descending';
        }

        if (sortType.includes('Alphabet')) {
            sortMethod = 'Alphabet';
        } else if (sortType.includes('Expected')) {
            sortMethod = 'Expected';
        }
        const inputparam = {
            gallerypath: imgpath,
            imtype: imtype,
            sortDir: sortDir,
            sortMethod: sortMethod,
        }
        console.log(inputparam)
        fetch('./display_images.php', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(inputparam) // 送信するデータをJSON形式で設定
        })
        .then(response => response.json()) // JSONとしてレスポンスを解析
        .then(images => {
            
            globalImagePath = images.map((image) => image.imagePath);
            const companyName = images.map((image) => image.CompanyName);
            const symbols = images.map((image) => image.Symbol);
            console.log(globalImagePath)
            const titleContainer = document.getElementById('image-title'); 
            titleContainer.innerHTML = '';
            const titlehandle = document.createElement('h1');
            titlehandle.textContent = imgpath;
            titleContainer.appendChild(titlehandle)
            const secondTitle = document.getElementById('second-title')
            secondTitle.textContent = dirname;

            const imageContainer = document.getElementById('image-container'); 
            imageContainer.innerHTML = ''; 
            const buttonLabels = ['a', 'b', 'c', 'd','etc'];
            globalImagePath.forEach((imagePath , index)=> {
                const inputElement = document.createElement('div');
                inputElement.className = 'classification';
                inputElement.name = "image_path";
                inputElement.value = imagePath; 
                inputElement.classList.add('portrait')
                imageContainer.appendChild(inputElement);
                const addlabel = document.createElement('label');
                addlabel.textContent = symbols[index] + ':' + companyName[index];
                addlabel.className='imglabel';
                inputElement.appendChild(addlabel)
                const imgElement = document.createElement('img');
                imgElement.src = imagePath;
                imgElement.alt = "Image";
                imgElement.style.width = "100%"
                inputElement.appendChild(imgElement);
            
            });
        
        })
        .catch(error => {
            console.error('Error fetching images:', error);
        });
        window.scrollTo(0,0);
    }

    function setupPage() {
        var e = (window.event)? window.event : arguments.callee.caller.arguments[0];
        var self = e.target || e.srcElement;
        const pm = self.dataset.pm
        const dirHandle = document.getElementById('directory')
        var currentIndex = dirHandle.selectedIndex;
        if (pm == '++') {
            currentIndex++;
            dirHandle.selectedIndex = currentIndex;
        } else {
            currentIndex--;
            dirHandle.selectedIndex = currentIndex;
        }
        displayImages();
    }
    function controllImage(addButton, label, imagePath) {
        console.log(label)
    }

    function update_news() {
        fetch('login/news.json')
            .then(response => response.json())
            .then(jsonData => {
                // タイムスタンプが一番新しいコメントを探す
                const latestComment = jsonData.reduce((latest, current) => {
                    return new Date(current.timestamp) > new Date(latest.timestamp) ? current : latest;
                });
                console.log(latestComment)
                // お知らせを表示
                document.getElementById('news').innerHTML = "[" + latestComment.timestamp + "]<br>   " + latestComment.comments;
                // document.getElementById('news').textContent = "[" + latestComment.timestamp + "]  " + latestComment.comments;
            })
            .catch(error => {
                console.error('JSONファイルの読み込みに失敗しました:', error);
            });
    }
    update_news();

    function getWeekday(date, lang) {
        var list = {
            ja: ["日", "月", "火", "水", "木", "金", "土"],
            en: ["SUN.", "Mon.", "Tue.", "Wed.", "The.", "Fri.", "Sat."]
        }
        //dateチェック
        if (date == undefined || date == "") {
            date = new Date().getDay();
        } else if (date.constructor.name == "Date") {
            date = date.getDay();
        } else if (!Number.isInteger(date)) {
            return "第一引数が不正です。";
        } else if (date < 0 || date > 6) {
            return "第一引数が不正です。";
        } else {
            date = Number(date);
        }

        if (lang == undefined || lang == "") {
            lang = "ja";
        } else if (lang != "ja" && lang != "en") {
            return "第二引数が不正です。";
        }
        return list[lang][date];
    }

</script>
</html>
