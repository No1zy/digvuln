
<h2>ユーザー検索画面</h2>

<form method="post">
    <p><label>ユーザー名: <input type="text" name="id"></label></p>
    <p><input type="submit" value="検索"></p>
</form>
<?php
if (!isset($_POST["id"])){
    echo "検索する文字列を入力してください";
    return;
}
$id = $_POST["id"];

$mysqli = new mysqli("localhost", "root", "", "rensyuu3");

if ($mysqli->connect_error) {
    echo $mysqli->connect_error;
    exit();
} else {
    $mysqli->set_charset("utf8");
}

$sql = "SELECT user_id FROM users WHERE user_id like '%$id%'";
if($result = $mysqli->query($sql)){
    echo "<p>" . "検索結果". "</p>";
    while ($row = $result->fetch_assoc()) {
        echo $row["user_id"] . "<br>";
    }
}

// DB接続を閉じる
$mysqli->close();

?>
