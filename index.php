<?php
/**
 * Created by PhpStorm.
 * Date: 2018-06-18
 * Time: 19:52
 */
session_start();

function readFileByLine(){
    $file = fopen("website.txt", "r") or exit("无法打开文件!");
    // 读取文件每一行，直到文件结尾
    $websites = array();
    while(!feof($file))
    {
        $web = fgets($file);
        if(!empty($web)){
            $websites[] = str_replace("\r\n","",$web);
        }
    }
    $_SESSION['websites'] = $websites;
    fclose($file);
}

function writeFile(){
    $file = fopen("website.txt","w+");
    $websites = $_SESSION['websites'];
    foreach ($websites as $website) {
        fwrite($file,$website."\r\n");
    }
    fclose($file);
}

function delete($id){
    array_splice($_SESSION['websites'],$id,1);
    writeFile();
}

function addWebsite($url, $phone){
    $file = fopen("website.txt","a");
    fwrite($file,$url." ");
    fwrite($file,$phone."\r\n");
    fclose($file);
}

// 操作
if (isset($_POST['api'])){
    $api = $_POST['api'];
    switch ($api){
        case 'get':
            readFileByLine();
            echo json_encode($_SESSION['websites']);
            break;
        case 'add':
            $url = $_POST['url'];
	    $pho = $_POST['phone'];
            addWebsite($url, $pho);
            break;
        case 'delete':
            $id = $_POST['id'];
            delete($id);
            break;
        case 'change':
            $id = $_POST['id'];
            $url = $_POST['url'];
            $websites = $_SESSION['websites'];
            $websites[$id] = $url;
            $_SESSION['websites'] = $websites;
            writeFile();
            break;
    }

    exit();
}

?>

<!doctype html>
<html lang="zh-cn">
<head>
    <meta charset="UTF-8">
    <meta name="viewport"
          content="width=device-width, user-scalable=no, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <link href="https://cdn.bootcss.com/bootstrap/4.1.1/css/bootstrap.min.css" rel="stylesheet">
    <title>打卡设置</title>
    <style>
        body, html{
            max-width: 800px;
            margin: 0 auto;
        }
        .list-group-item a{
            margin-right: 20px;
        }
    </style>
</head>
<body>
<div class="card">
    <h5 class="card-header">增加人员</h5>
    <div class="card-body">
        <div class="form-group">
            <label for="exampleInputPassword1">学号：</label>
            <input type="text" class="form-control" id="stuid" placeholder="学号">
            <label for="exampleInputPassword1">联系方式：</label>
             <input type="text" class="form-control" id="phone" placeholder="邮箱">
        </div>
        <a href="#" class="btn btn-primary" onclick="addWebsite()">增加</a>
    </div>
</div>



<script src="https://cdn.bootcss.com/jquery/3.3.1/jquery.min.js"></script>
<script src="https://cdn.bootcss.com/bootstrap/4.1.1/js/bootstrap.bundle.min.js"></script>
<script src="https://cdn.bootcss.com/bootstrap/4.1.1/js/bootstrap.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/es5-shim/4.5.7/es5-shim.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/es5-shim/4.5.7/es5-sham.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/json3/3.3.2/json3.min.js"></script>
<script src="template-web.js"></script>
<script src="layer/layer.js"></script>
<script>
    var websites = new Array();

    
    
    function addWebsite() {
        var website = $("#stuid").val();
	    var phone = $("#phone").val();
        if (website != "" && phone != "" &&website.length == 12 && (phone.length == 11 || phone.search('@') != -1)){
            $.ajax({
                url: 'index.php',
                type: 'POST',
                dataType: 'html',
                data:{api:'add', url:website, phone:phone},
                success:function () {
                    $("#website").val("");
                    layer.msg("增加成功");
                    
                }
            });
        } else{
            alert("请填写正确信息");
        }
    }
</script>

<footer>
  <p>仅供学习交流使用</p>
  <p>开源地址: <a href="https://github.com/ranxuebin/LZU_Quick_Check-in">GitHub</a></p>
</footer>
</body>
</html>


