import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

table_click_js = """
document.getElementsByTagName('tbody')[0].querySelectorAll('tr').forEach((row, index) => {
    row.addEventListener("dblclick", function(event) {
        row.style.color='red';    
        window.clickedRowIndex = index;
        window.clickedRow = row;           
    }, true);
});
"""

prompt_js = """
    document.body.setAttribute("data-balance", "");
    var a = prompt('Please enter balance:', '');
    document.body.setAttribute("data-balance", a);
"""
def get_clicked_row_and_index(driver):
    clicked_row_index = driver.execute_script("return window.clickedRowIndex;")
    clicked_row = driver.execute_script("return window.clickedRow;")
    return clicked_row, clicked_row_index

def show_prompt_balance(driver):
    driver.execute_script(prompt_js)
    while EC.alert_is_present()(driver):
        time.sleep(1)
    entered_text = driver.find_element(By.TAG_NAME, 'body').get_attribute('data-balance')        
    print('ACTION: Input balance')
    return entered_text

def get_init_data(driver):
    print(" There is no Init Data on Server, waiting...")
    driver.execute_script("alert('There is no init data in aggregator. Please double click.');")
    while EC.alert_is_present()(driver):
        time.sleep(1)

    clicked_row_index = -1
    while True:
        driver.execute_script(table_click_js)
        time.sleep(1)        
        clicked_row, clicked_row_index = get_clicked_row_and_index(driver)

        if clicked_row:
            print('ACTION: double clicked the row')
            break
        else:
            continue

    print(f"Index of the clicked row: {clicked_row_index}")
    balance = show_prompt_balance(driver)
    return clicked_row_index, balance

