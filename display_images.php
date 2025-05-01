<?php
// $raw = $argv[1]; // debug mode
// $data = json_decode($raw, true);
// $dir = $data['gallerypath'];
// $imtype = $data['imtype'];
// $sortDir = $data['sortDir'];
// $sortMethod = $data['sortMethod'];
$raw = file_get_contents('php://input');// Normal Mode
if ($raw === false) {
    die('Error input php!!!'); 
}
$data = json_decode($raw);
$dir = $data->gallerypath;
$imtype = $data->imtype;
$sortDir = $data->sortDir;
$sortMethod=$data->sortMethod;



// 共通部分
if ($imtype === 'prediction') {
    $includestr='*_figure.png';
    $sep='_';
} else if ($imtype === 'mpf30days') {
    $includestr='*-last30d.png';
    $sep='-';
}


if (strtolower($imtype) === 'prediction') {
    $includestr = '*_figure.png';
    $sep='_';
} else if (strtolower($imtype) === 'mpf30days') {
    $includestr = '*-last30d.png';
    $sep='-';
}



// read csv
function readCSV($filename) {
    $data = [];
    if (($handle = fopen($filename, 'r')) !== false) {
        $header = fgetcsv($handle);
        // while (($row = fgetcsv($handle)) !== false) {
            // $data[] = array_combine($header, $row);
        // }
        for ($i = 0; $i < 2; $i++) { //first 2row
            if (($row = fgetcsv($handle)) !== false) {
                $data[] = array_combine($header, $row);
            }
        }
        fclose($handle);
    // } else {
        // echo "Could NOT open csv file.";
    }
    return $data;
}

$LIST = [];

if (($handle = fopen('Symbol_List_Info.csv', 'r')) !== false) {
    $header =fgetcsv($handle);
    while (($row = fgetcsv($handle)) !== false) {
        $LIST[] = array_combine($header, $row);
    }
    fclose($handle);
}
function getCompanyNameBySymbol($symbol, $LIST) {
    foreach ($LIST as $item) {
        if ($item['Symbol'] === $symbol) {
            return $item['FullName']; 
        }
    }
    return null; 
}


$images = array();
if ($handle = opendir($dir)) {
    while (false !== ($file = readdir($handle))) {
        if ($file !== '.' && $file !== '..' && fnmatch($includestr, $file)) {
            $filepath = $dir . '/' . $file;
            $symbol = explode($sep, $file)[0];
            $Name = getCompanyNameBySymbol($symbol,$LIST);
            $csvfilename=$dir . '/' . str_replace(" ","\ ",$symbol) . '_tmp.csv';
            // echo $csvfilename . "\n";
            $arrycsv=readCSV($csvfilename);
            $images[] = array(
                'imagePath' => $filepath,
                'Expected' => $arrycsv[0]['future'] - $arrycsv[1]['future'],
                'Symbol' => $symbol,
                'CompanyName' => $Name,
            );
        }
    }
    closedir($handle);
}
usort($images, function($a, $b) {
    return $a['Expected'] <=> $b['Expected']; // spaceship operatorを使用
});
if ($sortMethod === 'Alphabet') {
    if (fnmatch('ascend*', $sortDir)) {
        usort($images, function($a, $b) {
            return strcmp($a['imagePath'], $b['imagePath']); 
        });
    } else {
        usort($images, function($a, $b) {
            return strcmp($b['imagePath'], $a['imagePath']); 
        });
    }
} else if ($sortMethod == 'Expected') {
    if (fnmatch('ascend*', $sortDir)) {
        usort($images, function($a, $b) {
            return $a['Expected'] <=> $b['Expected']; // spaceship operatorを使用
        });
    } else {
        usort($images, function($a, $b) {
            return $b['Expected'] <=> $a['Expected']; // spaceship operatorを使用
        });
    }
}

header('Content-Type: application/json');
echo json_encode($images, JSON_UNESCAPED_SLASHES);
?>
