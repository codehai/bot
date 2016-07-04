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
			String content = new String(Files.readAllBytes((new File("2.cookie.json")).toPath()));
			System.out.println(content);
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
			//String imgpath = "/home/hao/桌面/selenium/";
			//for(;;){		
				driver.get("http://192.168.2.100:1500");
				String mission = driver.findElement(By.tagName("pre")).getText();
				System.out.println(mission);
				JSONArray missionArray = new JSONArray(mission);
				JavascriptExecutor jse = (JavascriptExecutor)driver;
				driver.get("http://tieba.baidu.com");
				for( int i=0;i<jsonArray.length();i++ ){
					JSONObject jsonObject = jsonArray.getJSONObject(i);
					String name = jsonObject.getString("name");
					String value = jsonObject.getString("value");
					System.out.println("name:"+name);
					System.out.println("value:"+value);
					org.openqa.selenium.Cookie cookie = new org.openqa.selenium.Cookie(name,value);
					driver.manage().addCookie(cookie);    
							
				}
				driver.navigate().refresh();
				jse.executeScript("return document.querySelector('div[lgoinprompt]').remove();");
				WebElement body =  driver.findElement(By.tagName("body"));
				Actions action = new Actions(driver); 
				action.moveToElement(body,30,180).doubleClick().perform();
				 //action.doubleClick().perform(); ;
				//jse.executeScript("$("[lgoinprompt='prompt']").remove()");

				
			//}
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
