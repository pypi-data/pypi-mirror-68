def login_to_internshala(browser):
  from getpass import getpass
  browser.get('https:/www.internshala.com')
  button = browser.find_element_by_xpath("//button[@data-target = '#login-modal' and @data-toggle = 'modal']")
  button.click()
  email = getpass('email or username')
  browser.find_element_by_id('modal_email').send_keys(email)
  password = getpass('password')
  browser.find_element_by_id('modal_password').send_keys(password)
  browser.find_element_by_id('modal_login_submit').click()
  print('Login Successfull')
  return browser
