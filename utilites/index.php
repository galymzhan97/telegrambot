<?php
		function connect_db() {
		$host_R="localhost";
        $login_R="root";
        $password_R="";
        $db_R='test';
        $charset ='UTF8';

		$dsn = "mysql:host=$host_R;dbname=$db_R;charset=$charset";
		$opt = array(
		    PDO::ATTR_ERRMODE            => PDO::ERRMODE_EXCEPTION,
		    PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC
		);
		
		$pdo = new PDO($dsn, $login_R, $password_R, $opt);
		return $pdo;
		}

		function positive() {
		$pdo = connect_db();
		$smt = $pdo->prepare("SELECT ttext FROM sortpos");
		$smt->execute();
		$results = $smt->fetchAll(PDO::FETCH_ASSOC);
		
		$fp = fopen("pos.txt", 'a');
		foreach($results as $key) 
		{
			$str_before = $key['ttext'];
			$str_before = preg_replace("/[!-~]|»|«|❤️|—/", "", $str_before);
			$str_after = preg_replace("/ {2,}/", "", $str_before);
			$test = fwrite($fp, $str_after);
		}


		if ($test) echo 'Данные в файл успешно занесены.';
		else echo 'Ошибка при записи в файл.';
		fclose($fp); 
		}


		function negative() {
		$pdo = connect_db();
		$smt = $pdo->prepare("SELECT ttext FROM sortneg");
		$smt->execute();
		$results = $smt->fetchAll(PDO::FETCH_ASSOC);
		
		$fp = fopen("neg.txt", 'a');
		foreach($results as $key) 
		{
			$str_before = $key['ttext'];
			$str_before = preg_replace("/[!-~]|»|«|❤️|—/", "", $str_before);
			$str_after = preg_replace("/ {2,}/", " ", $str_before);
			$test = fwrite($fp, $str_after);
		}


		if ($test) echo 'Данные в файл успешно занесены.';
		else echo 'Ошибка при записи в файл.';
		fclose($fp); 
		}
		

		negative();
		positive();