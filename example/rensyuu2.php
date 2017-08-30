<?php 
header ( "X-XSS-Protection: 0" );
session_start();

?>

<h2>名前を入力してください</h2>
<form method="post">
<input type="text" name="name">
<input type="submit" value="送信">
</form>

<?php
if ( isset($_POST["name"]) ){
    echo "ようこそ" . $_POST["name"] . "さん";
}
?>
