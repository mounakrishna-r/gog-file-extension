chrome.runtime.onInstalled.addListener(() => {
  console.log("GOG Viewer Installed");
});

// Optional toolbar button opens GOG Studio directly
chrome.action.onClicked.addListener((tab) => {
  chrome.tabs.create({
    url: "https://gog-file-extension.onrender.com"
  });
});