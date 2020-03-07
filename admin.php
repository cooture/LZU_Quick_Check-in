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
             <input type="text" class="form-control" id="phone" placeholder="邮箱或电话">
        </div>
        <a href="#" class="btn btn-primary" onclick="addWebsite()">增加</a>
    </div>
</div>

<div class="card">
    <h5 class="card-header">列表</h5>
    <div class="card-body">
        <ul class="list-group" id="website-list">
<!--            <li class="list-group-item">-->
<!--                <a target="_blank" href="http://www.baidu.com">http://www.baidu.com</a>-->
<!--                <button type="button" class="btn btn-primary" onclick="changeWebsite(1, 'http://www.baidu.com');">修改</button>-->
<!--                <button type="button" class="btn btn-danger" onclick="deleteWebsite(1);">删除</button>-->
<!--            </li>-->
        </ul>
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

    function getWebsites() {
        $.ajax({
           url: 'admin.php',
           type: 'POST',
           dataType: 'json',
           data:{api:'get'},
           success:function (result) {
                websites = result;
                updateList();
                console.log(result);
            }
        });
    }

    function updateList() {
        var data = {
            list: websites
        };
        var html = template('website-template', data);
        document.getElementById('website-list').innerHTML = html;
    }
    
    function addWebsite() {
        var website = $("#stuid").val();
	var phone = $("#phone").val();
        if (website != "" && phone != ""){
            $.ajax({
                url: 'admin.php',
                type: 'POST',
                dataType: 'html',
                data:{api:'add', url:website, phone:phone},
                success:function () {
                    $("#website").val("");
                    layer.msg("增加成功");
                    getWebsites();
                }
            });
        } else{
            alert("请填写信息");
        }
    }

    function deleteWebsite(id) {
        $.ajax({
            url: 'admin.php',
            type: 'POST',
            dataType: 'html',
            data:{api:'delete', id:id},
            success: function () {
                layer.msg("删除成功");
                getWebsites();
            }
        });
    }

    function changeWebsite(id, url) {
        layer.prompt({title: '请修改', value: url, formType: 2}, function(text, index){
            // layer.close(index);
            $.ajax({
                url: 'admin.php',
                type: 'POST',
                dataType: 'html',
                data:{api:'change', id:id, url:text},
                success: function () {
                    layer.msg("修改成功");
                    getWebsites();
                }
            });
        });
        getWebsites();
    }

    $(function () {
        getWebsites();
    });
</script>

<script id="website-template" type="text/html">
    {{each list value i}}
    <li class="list-group-item">
        <p target="_blank" href="{{value}}">{{value}}</a>
        <button type="button" class="btn btn-primary" onclick="changeWebsite({{i}}, '{{value}}');">修改</button>
        <button type="button" class="btn btn-danger" onclick="deleteWebsite({{i}});">删除</button>
    </li>
    {{/each}}
</script>
</body>
</html>


