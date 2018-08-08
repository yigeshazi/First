from selenium import webdriver

d=webdriver.Chrome()
url="https://www.baidu.com/"
d.get(url=url)
d.find_element_by_xpath('//*[@id="u1"]/a[7]').click()
d.find_element_by_xpath('//*[@id="TANGRAM__PSP_10__footerULoginBtn"]').click()
d.find_element_by_xpath('//*[@id="TANGRAM__PSP_10__userName"]').send_keys('wsmjiushiaini')
d.find_element_by_xpath('//*[@id="TANGRAM__PSP_10__password"]').send_keys('wang1989')
d.find_element_by_xpath('//*[@id="TANGRAM__PSP_10__submit"]').click()
d.find_element_by_css_selector('#u_sp > a:nth-child(5)').click()
d.find_element_by_css_selector('#j_u_username > div.u_ddl > div > div.u_ddl_con_top > ul > li.u_itieba > a').click()



