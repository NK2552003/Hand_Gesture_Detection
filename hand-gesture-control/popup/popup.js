document.addEventListener('DOMContentLoaded', () => {
    const toggle = document.getElementById('toggle');
    const status = document.getElementById('status');
  
    chrome.storage.local.get('isActive', (data) => {
      toggle.checked = data.isActive || false;
      status.textContent = toggle.checked ? 'ON' : 'OFF';
    });
  
    toggle.addEventListener('change', (e) => {
      const isActive = e.target.checked;
      status.textContent = isActive ? 'ON' : 'OFF';
      
      chrome.storage.local.set({ isActive });
      chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
        chrome.tabs.sendMessage(tabs[0].id, { action: 'toggle', isActive });
      });
    });
  });