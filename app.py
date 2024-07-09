from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import dotenv
import time
import pandas as pd


config = dotenv.dotenv_values(".env")

service = Service("C:/Users/cande/Downloads/chromedriver-win64/chromedriver-win64/chromedriver.exe")
driver = webdriver.Chrome(service=service)

driver.get("https://www.linkedin.com/home")

time.sleep(5)

userNameBox = driver.find_element(By.ID, "session_key")
userNameBox.send_keys(config["linkedin_email"])

passwordBox = driver.find_element(By.ID, "session_password")
passwordBox.send_keys(config["linkedin_password"])

passwordBox.send_keys(Keys.ENTER)

time.sleep(60)
url = "Linkedin_Post_URL"

driver.get(url)
time.sleep(5)

def moreCommentButton():
    try:
        if driver.find_element(By.CSS_SELECTOR, "button.comments-comments-list__load-more-comments-button.artdeco-button.artdeco-button--muted.artdeco-button--1.artdeco-button--tertiary.ember-view"):
            more_comment = driver.find_element(By.CSS_SELECTOR, "button.comments-comments-list__load-more-comments-button.artdeco-button.artdeco-button--muted.artdeco-button--1.artdeco-button--tertiary.ember-view")
            more_comment.click()
            time.sleep(15)
            moreCommentButton()
    except:
        print("more comment button not found")

def moreReplyButton():
    try:
        buttons = driver.find_elements(By.CSS_SELECTOR, "button.button.show-prev-replies.t-12.t-black.t-normal.hoverable-link-text")
        for button in buttons:
            button.click()
            time.sleep(5)
            moreReplyButton()
    except:
        print("more reply button not found")


def getName(sentence):
    splitedSentence = sentence.split()

    for i, k in enumerate(splitedSentence):
        if k == "View":
            return " ".join(splitedSentence[:i])

moreCommentButton()
moreReplyButton()

time.sleep(60)
commentAuthor = []
comments = driver.find_elements(By.CSS_SELECTOR, "article.comments-comment-item.comments-comments-list__comment-item")


commentText = []
replyAuthor = []
replyText = []
comment_Ids = []
replyCommentIds = []
counter = 1
comment_counter = 0
for comment in comments:
    comment_counter += 1
    print("---------------------------")
    commenter_name = comment.find_element(By.CSS_SELECTOR, "span.comments-post-meta__name-text.hoverable-link-text.mr1")
    commenter_name = getName(commenter_name.text)
    #print(commenter_name.find_elements(By.CSS_SELECTOR, "span")[0].text)
    comment_text = comment.find_element(By.CSS_SELECTOR, "span.comments-comment-item__main-content.feed-shared-main-content--comment.t-14.t-black.t-normal").text
    comment_replies = comment.find_elements(By.CSS_SELECTOR, "article.comments-comment-item.comments-reply-item.reply-item")
    comment_Ids.append(counter)
    commentAuthor.append(commenter_name)
    commentText.append(comment_text)

    print(commenter_name)
    print(comment_text)
    for reply in comment_replies:
        comment_counter += 1
        print("~~~~~~~~~~~~")
        reply_author = reply.find_element(By.CSS_SELECTOR, "span.comments-post-meta__name-text.hoverable-link-text.mr1")
        reply_author = getName(reply_author.text)
        reply_comment = reply.find_element(By.CSS_SELECTOR, "div.update-components-text.relative").text
        print(reply_author)
        print(reply_comment)
        replyCommentIds.append(counter)
        replyAuthor.append(reply_author)
        replyText.append(reply_comment)
        print("~~~~~~~~~~~~")
    print("---------------------------")
    counter += 1

comments_data = {
    "Comment ID": comment_Ids,
    "Comment Author": commentAuthor,
    "Comment Text": commentText
}

reply_data = {
    "Comment ID": replyCommentIds,
    "Reply Author": replyAuthor,
    "Reply Text": replyText
}

comment_df = pd.DataFrame(comments_data)
reply_df = pd.DataFrame(reply_data)

print(comment_df)
print(reply_df)

df = pd.merge(comment_df,reply_df, on="Comment ID", how="outer")

print(df)

df.to_csv("output.csv", index=False)
df.to_json("output.json")

print(comment_counter)
