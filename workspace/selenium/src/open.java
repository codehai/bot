import org.openqa.selenium.*;
import org.openqa.selenium.chrome.*;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.interactions.Actions; 
import org.openqa.selenium.support.ui.WebDriverWait;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.remote.*;
import org.sikuli.script.*;
import org.sikuli.basics.Debug;
import java.io.*;
import java.util.*;
import java.nio.file.Files; 
import java.nio.file.attribute.BasicFileAttributes;  
import java.nio.charset.StandardCharsets;  
import java.nio.file.Paths;
import org.json.*;
import java.sql.Connection; 
import java.sql.DriverManager; 
import java.sql.SQLException; 
import java.sql.Statement;
import java.sql.ResultSet; 

import java.text.SimpleDateFormat;


public class open{
	 public static boolean doesWebElementExist(WebDriver driver, By selector){ 
     		 	try { 
               				driver.findElement(selector); 
              				return true; 
         			} 
          			catch (org.openqa.selenium.NoSuchElementException e) { 
                 				return false; 
         			} 
 	}   
	public static void main(String[ ] args){
		
		/*String fullFileName = "2.cookie.json";
        		File file = new File(fullFileName);
        		Scanner scanner = null;
        		StringBuilder buffer = new StringBuilder();
		try {
			scanner = new Scanner(file, "utf-8");
			while (scanner.hasNextLine()) {
				buffer.append(scanner.nextLine());
			}

		} catch (FileNotFoundException e) {
		// TODO Auto-generated catch block  
		} finally {
			if (scanner != null) {
				scanner.close();
			}
		}*/
		try{
			try{   
    				//加载MySql的驱动类   
    				Class.forName("org.postgresql.Driver");   
    			}catch(ClassNotFoundException e){   
    				System.out.println("找不到驱动程序类 ，加载驱动失败！");   
    				e.printStackTrace() ;   
    			}
    			String url = "jdbc:postgresql://123.59.77.204:27213/dev?sslmode=require" ;    
     			String username = "tiebabot0" ;   
     			String password = "y53bnd573w4r" ; 
     			Connection con = null; 
    			try{   
    				con = DriverManager.getConnection(url , username , password ) ;   
     			}catch(SQLException se){   
    				System.out.println("数据库连接失败！");   
    				se.printStackTrace() ;   
     			}
     			
        			

    			/*
			String url = "jdbc:postgresql://123.59.77.204:27231/dev"; 
			try{ 
				conn = DriverManager.getConnection(url, "tiebabot0", "y53bnd573w4r"); 
			} 
			catch (SQLException e) { 
				e.printStackTrace(); 
			} 
        			String sql="select * from tieba"; 
        			Statement stmt=null; 
        			ResultSet rs=null; 
        			try { 
            				stmt=conn.createStatement(); 
            				rs=stmt.executeQuery(sql); 
				while(rs.next()){ 
                					System.out.println(rs.getInt(1)); 
            				} 
        			} 
        			catch (SQLException e) { 
            				e.printStackTrace(); 
        			} */
			String content = new String(Files.readAllBytes((new File("2.cookie.json")).toPath()));
			JSONArray jsonArray = new JSONArray(content);
			
			//JSONArray ja = new JSONArray(content);
			//String content = new String (Files.readAllLines(new File("2.cookie.json").toPath(),StandardCharsets.UTF_8));
			//String buffer = Files.toString(new File("2.cookie.json"),StandardCharsets.UTF_8);
			// String js = buffer.toString();
			// System.out.println(js);
			// JSONArray  ja = new JSONArray(js);
			// for ( i=0;ja.length();i++) {
			// 	JSONObject jo = JSONArray.getJSONObject(i);
			// 	System.out.println(jo.getString("domain"));
			// }
			//JSONObject jo = new JSONObject(js);
	        		//JSONArray ja = jo.getJSONArray("map");
	        		//System.out.println(jsonArray3);
			System.setProperty("webdriver.chrome.driver","../chromedriver");
			//FirefoxProfile profile = new FirefoxProfile();
			//profile.setPreference("general.useragent.override", "whatever you want");//useragent
			ChromeOptions options = new ChromeOptions();
			options.addArguments("--user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1");
			WebDriver driver = new ChromeDriver(options);
			Screen s  =  new Screen();
			WebDriverWait wait = new WebDriverWait(driver,30);
			//String imgpath = "/home/hao/桌面/selenium/";
			for(;;){		
				driver.get("http://192.168.2.100:1500");
				String mission = driver.findElement(By.tagName("pre")).getText();
				JSONArray missionArray = new JSONArray(mission);
				JavascriptExecutor jse = (JavascriptExecutor)driver;
				driver.get("http://tieba.baidu.com");
				for( int i=0;i<jsonArray.length();i++ ){
					JSONObject jsonObject = jsonArray.getJSONObject(i);
					String name = jsonObject.getString("name");
					String value = jsonObject.getString("value");
					org.openqa.selenium.Cookie cookie = new org.openqa.selenium.Cookie(name,value);
					driver.manage().addCookie(cookie);    
							
				}
				driver.navigate().refresh();
				driver.findElement(By.linkText("我")).click();
				wait.until(ExpectedConditions.visibilityOfElementLocated(By.className("user_info_name")));
				String user = driver.findElement(By.className("user_info_name")).getText();
				jse.executeScript("return document.querySelector('div[lgoinprompt]').remove();");
				//jse.executeScript("$("[lgoinprompt='prompt']").remove()");
				for(int j=0;j<missionArray.length();j++){

					JSONObject missionObj = missionArray.getJSONObject(j);
					String ba = missionObj.getString("ba");
					String huiString = missionObj.getString("hui");
					JSONObject huiObject = new JSONObject(huiString);
					int lou_min = Integer.parseInt(huiObject.getString("lou-min"));
					int lou_max = Integer.parseInt(huiObject.getString("lou-max"));
					String postString = huiObject.getString("posts");
					JSONArray postArray =  new JSONArray(postString);
					String contentSend = "";
					System.out.println("任务:在"+ba+"吧第"+lou_min+"到"+lou_max+"发帖"+postArray.length()+"个");
					for(int k=0;k<postArray.length();k++){
						String  contentString =  postArray.getString(k);
						JSONArray contentArray = new JSONArray(contentString);
						contentSend = contentArray.getString(0);
						String imgStr = contentArray.getString(1);
						JSONArray imgArr = new JSONArray(imgStr);
						String imgPath = imgArr.getString(1);
						Actions action = new Actions(driver); 
						if(doesWebElementExist(driver,By.cssSelector("a.top_search"))){
							//System.out.println("find top_search");
							WebElement topSearch = driver.findElement(By.cssSelector("a.top_search"));
							action.click(driver.findElement(By.cssSelector("a.top_search"))).perform();
							//s.click("search.png");
							//driver.findElement(By.cssSelector("a.top_search")).click();
						}else if(doesWebElementExist(driver,By.linkText("搜索"))){
							//System.out.println("find search_btn");
							WebElement search_btn = driver.findElement(By.linkText("搜索"));
							//action.click(driver.findElement(By.linkText("搜索"))).perform();
							action.moveToElement(search_btn).click().perform();
							//search_btn.click();
							//s.click("search1.png");
							//driver.findElement(By.cssSelector("a.search_btn")).click();
						}else if(doesWebElementExist(driver,By.cssSelector("a.blue_kit_icon_search"))){
							//System.out.println("find search_btn");
							WebElement icon_search = driver.findElement(By.cssSelector("a.blue_kit_icon_search"));
							action.click(driver.findElement(By.cssSelector("a.blue_kit_icon_search"))).perform();		
							//s.click("search2.png");
							//driver.findElement(By.cssSelector("a.blue_kit_icon_search")).click();
						}
						/*
						if(doesWebElementExist(driver,By.className("daoliu_sign_in_prompt_close"))){
							//System.out.println("find search_btn");
							//s.click("search1.png");
							WebElement  element = driver.findElement(By.className("daoliu_sign_in_prompt_close"));
							Actions actions = new Actions(driver);
							actions.moveToElement(element).click().perform();
							//driver.findElement(By.className("daoliu_sign_in_prompt_close")).click();
						}*/
						
						wait.until(ExpectedConditions.visibilityOfElementLocated(By.tagName("input")));
						driver.findElement(By.tagName("input")).sendKeys(ba);
						
						//s.click("enter.png",0);
						wait.until(ExpectedConditions.visibilityOfElementLocated(By.id("btn")));
						action.click(driver.findElement(By.id("btn"))).perform();
						wait.until(ExpectedConditions.visibilityOfElementLocated(By.className("btn_icon")));
						jse.executeScript("return document.getElementById('app-special').remove();");
						
						List <WebElement> tl = driver.findElements(By.className("tl_shadow"));
						List <WebElement> btn = driver.findElements(By.className("btn_icon"));

						int maxFloor = 0;
						jse.executeScript("return document.querySelector('div[lgoinprompt]').remove();");
						for(int i=0;i<btn.size();i++){
							int btn_num_i;
							String btn_num = btn.get(i).getText();
							if(btn_num.equals("回复")){
								btn_num_i = 0;
							}
							else{
								btn_num_i = Integer.parseInt(btn_num);
							}
							//System.out.println(btn_num_i);
							if(btn_num_i<30&&btn_num_i>=0){
								maxFloor++;
							}
						};
						//driver.findElement(By.className("daoliu_sign_in_prompt_close")).click();
						jse.executeScript("return document.querySelector('button.frs_pb_leadapp_pop_close').click();");
						//System.out.println(doesWebElementExist(driver,By.cssSelector("button.daoliu_sign_in_prompt_close")));
						/*if(doesWebElementExist(driver,By.cssSelector("button.daoliu_sign_in_prompt_close"))){
							//System.out.println("find search_btn");
							action.click(driver.findElement(By.cssSelector("button.daoliu_sign_in_prompt_close"))).perform();
							//s.click("search2.png");
							//driver.findElement(By.cssSelector("a.blue_kit_icon_search")).click();
						}*/
						int targetFloor =1+(int)(Math.random()*maxFloor);
						int resultFloor = 0 ;
						String title = "";
						for(int i=0;i<btn.size();i++){
							String btn_num = btn.get(i).getText();
							int btn_num_i;
							if(btn_num.equals("回复")){
								btn_num_i = 0;
							}
							else{
								btn_num_i = Integer.parseInt(btn_num);
							}
							if(btn_num_i<30&&btn_num_i>=0){
								resultFloor++;
								if(resultFloor==targetFloor){
									//System.out.println("find target:"+i);
									SimpleDateFormat df = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");//设置日期格式
									String date = df.format(new Date());
									System.out.println(df.format(new Date()));// new Date()为获取当前系统时间
									System.out.println(tl.get(i).findElement(By.className("ti_title")).findElement(By.tagName("span")).getText());
									title = tl.get(i).findElement(By.className("ti_title")).findElement(By.tagName("span")).getText();
									FileWriter fileWriter=new FileWriter("Result.txt", true); // true代表追加
									fileWriter.write(date);
									//tl.get(i).findElement(By.tagName("a")).click();
									tl.get(i).findElement(By.cssSelector("div.btn_reply")).click();
									break;	
								}
							}
						}
						//wait.until(ExpectedConditions.visibilityOfElementLocated(By.cssSelector("div[lgoinprompt]")));
						//jse.executeScript("return document.querySelector('div[lgoinprompt]').remove();");
						wait.until(ExpectedConditions.visibilityOfElementLocated(By.cssSelector("a.btn_reply")));

						//jse.executeScript("return document.querySelector('div[lgoinprompt]').style.display='none';");

						/*driver.findElement(By.cssSelector("a.btn_reply")).click();
						wait.until(ExpectedConditions.visibilityOfElementLocated(By.tagName("textarea")));
						driver.findElement(By.tagName("textarea")).sendKeys(contentSend);
						driver.findElement(By.className("multi")).findElement(By.className("upload-input")).sendKeys(imgPath);*/

						List <WebElement> postList = driver.findElement(By.id("pblist")).findElements(By.className("post_list_item"));
						for(int p = 0;p<postList.size();p++){
							String postContent = postList.get(p).findElement(By.className("content")).getText();

							System.out.println(postContent);
							if(postContent.length()<100&&postContent.length()>1){
								String sql="insert into tieba values(\'"+ba+"\',\'"+title+"\',\'"+postContent+"\')";
								System.out.println(sql);
	     							Statement stmt=null; 
	        							ResultSet rs=null;
				        				try { 
				            					stmt=con.createStatement(); 
				            					rs=stmt.executeQuery(sql); 
				            			
				        				} 
				        				catch (SQLException e) { 
				            					e.printStackTrace(); 
				        				} 
							}
						}
						//driver.findElement(By.className("pb_poster_layer")).findElement(By.className("j_submit_btn")).click();
						//wait.until(ExpectedConditions.visibilityOfElementLocated(By.className("blue_kit_right")));
						//driver.findElement(By.className("pb_poster_layer")).findElement(By.className("blue_kit_right")).findElement(By.tagName("a")).click();
						/*WebElement element = driver.findElement(By.className("pb_poster_layer")).findElement(By.className("blue_kit_right")).findElement(By.tagName("a"));
						Actions actions = new Actions(driver);
						actions.moveToElement(element).click().perform();*/
						//s.click("fabiao.png");

						//WebElement postLayer = driver.findElement(By.className("pb_poster_layer"));
						//WebElement kitRight = postLayer.findElement(By.className("blue_kit_right"));
						//WebElement fabiao = kitRight.findElement(By.tagName("a"));

						//System.out.println("fabiao:"+fabiao.getText());
						//kitRight.findElement(By.tagName("a")).click();
						//action.moveToElement(kitRight).perform();
						//action.click().perform();
						//wait.until(ExpectedConditions.visibilityOfElementLocated(By.cssSelector("div.pb_poster_layer div.blue_kit_right")));
						//s.click("huifu.png");
						//driver.findElement(By.linkText("发表")).click();
						//action.moveToElement(driver.findElement(By.cssSelector("div.pb_poster_layer div.blue_kit_right"))).click();
						//driver.findElement(By.cssSelector("div.pb_poster_layer a.j_submit_btn")).click();

						/*jse.executeScript("return document.querySelector('div.pb_poster_layer div.blue_kit_right a.j_submit_btn').click();");*/
						wait.until(ExpectedConditions.visibilityOfElementLocated(By.linkText("主题贴")));
						action.click(driver.findElement(By.cssSelector(".blue_kit_left a.blue_kit_btn_back"))).perform();
						wait.until(ExpectedConditions.visibilityOfElementLocated(By.linkText(ba+"吧")));

						//action.click(driver.findElement(By.cssSelector("a.blue_kit_icon_search"))).perform();
						//action.click(driver.findElement(By.cssSelector(".blue_kit_left a.blue_kit_btn_back"))).perform();
						//s.click("back.png");
						//s.click("back.png");	
					}
				}	
			}
		}catch(IOException e){
			System.out.println("12345");
		}catch(JSONException e){
			System.out.println(e);
		}/*catch(FindFailed e){
			System.out.println(e);
		}*//*catch(InterruptedException e){
			System.out.println(e);
		}*/
	}
}
