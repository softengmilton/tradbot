/**
 * Chrome Storage Service
 * Handles persistent storage using Chrome's storage API
 */

type StorageValue = string | number | boolean | Record<string, any> | any[];

interface StorageResult {
  success: boolean;
  data?: StorageValue;
  error?: string;
}

export const storageService = {
  /**
   * Get a value from storage
   */
  get: async (key: string): Promise<StorageValue | undefined> => {
    return new Promise((resolve, reject) => {
      try {
        chrome.storage.local.get(key, (result) => {
          if (chrome.runtime.lastError) {
            reject(new Error(chrome.runtime.lastError.message));
          } else {
            resolve(result[key]);
          }
        });
      } catch (error) {
        reject(error);
      }
    });
  },

  /**
   * Set a value in storage
   */
  set: async (key: string, value: StorageValue): Promise<boolean> => {
    return new Promise((resolve, reject) => {
      try {
        chrome.storage.local.set({ [key]: value }, () => {
          if (chrome.runtime.lastError) {
            reject(new Error(chrome.runtime.lastError.message));
          } else {
            resolve(true);
          }
        });
      } catch (error) {
        reject(error);
      }
    });
  },

  /**
   * Remove a key from storage
   */
  remove: async (key: string): Promise<boolean> => {
    return new Promise((resolve, reject) => {
      try {
        chrome.storage.local.remove(key, () => {
          if (chrome.runtime.lastError) {
            reject(new Error(chrome.runtime.lastError.message));
          } else {
            resolve(true);
          }
        });
      } catch (error) {
        reject(error);
      }
    });
  },

  /**
   * Clear all storage
   */
  clear: async (): Promise<boolean> => {
    return new Promise((resolve, reject) => {
      try {
        chrome.storage.local.clear(() => {
          if (chrome.runtime.lastError) {
            reject(new Error(chrome.runtime.lastError.message));
          } else {
            resolve(true);
          }
        });
      } catch (error) {
        reject(error);
      }
    });
  },

  /**
   * Get multiple values from storage
   */
  getMultiple: async (keys: string[]): Promise<Record<string, StorageValue>> => {
    return new Promise((resolve, reject) => {
      try {
        chrome.storage.local.get(keys, (result) => {
          if (chrome.runtime.lastError) {
            reject(new Error(chrome.runtime.lastError.message));
          } else {
            resolve(result);
          }
        });
      } catch (error) {
        reject(error);
      }
    });
  },
};
