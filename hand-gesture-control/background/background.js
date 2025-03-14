chrome.runtime.onInstalled.addListener(() => {
  console.log("Hand Gesture Control Extension Installed");
});

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.action === "scroll") {
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
      chrome.scripting.executeScript({
        target: { tabId: tabs[0].id },
        function: scrollPage,
        args: [message.direction, message.amount],
      });
    });
  } else if (message.action === "switchTab") {
    chrome.tabs.query({ currentWindow: true }, (tabs) => {
      const currentIndex = tabs.findIndex((tab) => tab.active);
      const nextIndex = message.direction === "next" ? currentIndex + 1 : currentIndex - 1;
      if (nextIndex >= 0 && nextIndex < tabs.length) {
        chrome.tabs.update(tabs[nextIndex].id, { active: true });
      }
    });
  }
});

function scrollPage(direction, amount) {
  window.scrollBy(0, direction === "up" ? -amount : amount);
}