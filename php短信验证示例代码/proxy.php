<?php
	
if(isset($_POST)&&isset($_POST['rand_code'])&&isset($_POST['identifier']))
{
    $randcode = $_POST['rand_code'];
    $identifier = $_POST['identifier'];
    header("Cache-Control:no-stroe,no-cache,must-revalidate,post-check=0,pre-check=0");
    header("Pragma:no-cache");
    echo json_encode(array('res_code'=>0));
    exit();
}

?>
