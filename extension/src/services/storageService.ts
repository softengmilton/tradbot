export const storageService = {
  get: async (key: string) => {
    return new Promise((resolve) => {
      chrome.storage.local.get(key, (result) => {
        resolve(result[key]);
      });
    });
  },

  set: async (key: string, value: any) => {
    return new Promise((resolve) => {
      chrome.storage.local.set({ [key]: value }, () => {
        resolve(true);
      });
    });
  },

  remove: async (key: string) => {
    return new Promise((resolve) => {
      chrome.storage.local.remove(key, () => {
        resolve(true);
      });
    });
  },

  clear: async () => {
    return new Promise((resolve) => {
      chrome.storage.local.clear(() => {
        resolve(true);
      });
    });
  },
};
