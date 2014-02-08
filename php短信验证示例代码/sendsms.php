<?php
header("Content-Type: text/html; charset=utf-8");
if(isset($_POST)&&isset($_POST['app_id'])&&isset($_POST['app_secret'])&&isset($_POST['access_token']))
{   
    $timestamp = date('Y-m-d H:i:s');
    $app_id = $_POST['app_id'];
    $app_secret = $_POST['app_secret'];
    $access_token = $_POST['access_token'];
    if(isset($_POST['btn_token']))
    {
        $url = "http://api.189.cn/v2/dm/randcode/token?";

        $param['app_id']= "app_id=".$app_id;
        $param['access_token'] = "access_token=".$access_token;
        $param['timestamp'] = "timestamp=".$timestamp;
        ksort($param);
        $plaintext = implode("&",$param);
        $param['sign'] = "sign=".rawurlencode(base64_encode(hash_hmac("sha1", $plaintext, $app_secret, $raw_output=True)));
        ksort($param);
        $url .= implode("&",$param);
        $result = curl_get($url);
        $resultArray = json_decode($result,true);
        $token = $resultArray['token'];
    }
    #获取验证码
    else if(isset($_POST['btn_send']))
    {
        $url = "http://api.189.cn/v2/dm/randcode/send";
        $token = $_POST['token'];
        $phone = $_POST['phone'];
        $dataurl = $_POST['url'];
        $exp_time = $_POST['exptime'];
        
        $param['app_id']= "app_id=".$app_id;
        $param['access_token'] = "access_token=".$access_token;
        $param['timestamp'] = "timestamp=".$timestamp;
        $param['token'] = "token=".$token;
        $param['phone'] = "phone=".$phone;
        $param['url'] = "url=".$dataurl;
        if(isset($exp_time))
            $param['exp_time'] = "exp_time=".$exp_time;
        ksort($param);
        $plaintext = implode("&",$param);
        $param['sign'] = "sign=".rawurlencode(base64_encode(hash_hmac("sha1", $plaintext, $app_secret, $raw_output=True)));
        ksort($param);
        $str = implode("&",$param);
        $result = curl_post($url,$str);
        $resultArray = json_decode($result,true);
	
    }
}


function curl_get($url='', $options=array()){
    $ch = curl_init($url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
    curl_setopt($ch, CURLOPT_TIMEOUT, 5);
    if (!empty($options)){
        curl_setopt_array($ch, $options);
    }
    $data = curl_exec($ch);
    curl_close($ch);
    return $data;
}

function curl_post($url='', $postdata='', $options=array()){
    $ch = curl_init($url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
    curl_setopt($ch, CURLOPT_POST, 1);
    curl_setopt($ch, CURLOPT_POSTFIELDS, $postdata);
    curl_setopt($ch, CURLOPT_TIMEOUT, 5);
    if (!empty($options)){
        curl_setopt_array($ch, $options);
    }
    $data = curl_exec($ch);
    curl_close($ch);
    return $data;
}

?>

<html>
<head>
<title>短信验证码示例</title>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
<script>
   function checktoken()
   {
	if(document.getElementById('app_id').value == "")
        {    
            alert('请填写AppID！');
            return false;
        } 
        else if(document.getElementById('app_secret').value == "")
	{
	    alert('请填写AppSecret!')
	    return false;
	}
	else if(document.getElementById('access_token').value=="")
	{
	    alert('请填写Access_Token!');
	    return false;
	}
	else 
	    return true;
    }
   function checksend()
   {
	if(document.getElementById('app_id').value == "")
        {    
            alert('请填写AppID！');
            return false;
        } 
        else if(document.getElementById('app_secret').value == "")
	{
	    alert('请填写AppSecret!')
	    return false;
	}
	else if(document.getElementById('access_token').value=="")
	{
	    alert('请填写Access_Token!');
	    return false;
	}
        if(document.getElementById('token').value == "")
        {    
            alert('请先获取信任码！');
            return false;
        } 
        else if(document.getElementById('phone').value=="")
        {
          	alert('请输入手机号码！');
          	return false;
        }
     	else if(document.getElementById('url').value=="")
        {
        	alert('请输入接收发送状态的URL!');
            return false;
        }
     	else 
          return true;
   }
</script>
</head>

<body>
    <h2 style="text-align:center">天翼开放平台短信验证码示例程序 for PHP</h2>
    <div style ="padding-left:30px">
	<a href="sms.rar">下载示例程序代码</a>	
    </div>
    <form id="token_form" method="post" action="sendsms.php">
         <div style="margin-top:50px">
           <fieldset>
                <legend>用户基本信息</legend>
                AppID:<input id="app_id" name="app_id" type="text" value="<?php echo $app_id?>" />
                AppSecret:<input id="app_secret" name="app_secret" type="text" value="<?php echo $app_secret ?>" />
                Access_Token:<input id="access_token" name="access_token" type="text" value = "<?php echo $access_token ?>" />
           </fieldset>
         </div>
        <div style="margin-top:50px">
            <fieldset>
                <legend>短信验证码设置</legend>
		<p><b>第一步:</b>
		<input name="btn_token" type="submit" value="获取信任码" onclick="return checktoken();" /></p>
		<p><b>第二步:</b>
                Token:<input id="token" name="token" type="text" value="<?php echo $token ?>" />
                Phone:<input id="phone" name="phone" type="text" value="<?php echo $phone ?>" />
                URL:<input id="url" name="url" type="text" value="http://101.227.251.180:10001/open189/sms/proxy.php"/>
                Expire Time:<input name="exptime" type="text"/>
                <input name="btn_send" type="submit" value="下发短信" onclick="return checksend();" />
                </p>
	     </fieldset>
        </div>
        <div id="div_result" style="margin-top:40px;height:80px;">
	    <fieldset style="height:50px;">
		<legend>响应结果</legend>
		<?php echo $result;?>
	    </fieldset>
	</div>
	<div id="div_description">
		<p>注：在URL中填写的地址为应用发监听地址，用于接收和反馈验证参数。 
		       Expire Time为验证码过期时间，可留空，留空状态默认为2分钟。
	</div>
    </form>
</body>
</html>