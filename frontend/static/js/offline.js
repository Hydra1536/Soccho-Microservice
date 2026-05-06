// Offline support - IndexedDB
const DB_NAME = 'soccho';
const DB_VERSION = 1;
const STORES = {
  TRANSACTIONS: 'transactions',
  NOTIFICATIONS: 'notifications'
};

class OfflineStorage {
  constructor() {
    this.db = null;
  }

  async init() {
    return new Promise((resolve, reject) => {
      const request = indexedDB.open(DB_NAME, DB_VERSION);
      
      request.onerror = () => reject(request.error);
      request.onsuccess = () => {
        this.db = request.result;
        resolve();
      };
      
      request.onupgradeneeded = (e) => {
        const db = e.target.result;
        db.createObjectStore(STORES.TRANSACTIONS, { keyPath: 'id', autoIncrement: true });
        db.createObjectStore(STORES.NOTIFICATIONS, { keyPath: 'id', autoIncrement: true });
      };
    });
  }

  async queueTransaction(tx) {
    const trans = this.db.transaction(STORES.TRANSACTIONS, 'readwrite');
    const store = trans.objectStore(STORES.TRANSACTIONS);
    return store.add({ ...tx, queuedAt: Date.now() });
  }

  async getQueuedTransactions() {
    const trans = this.db.transaction(STORES.TRANSACTIONS, 'readonly');
    const store = trans.objectStore(STORES.TRANSACTIONS);
    return store.getAll();
  }

  async clearQueue(storeName) {
    const trans = this.db.transaction(storeName, 'readwrite');
    const store = trans.objectStore(storeName);
    return store.clear();
  }
}

const offlineStorage = new OfflineStorage();

document.addEventListener('DOMContentLoaded', () => {
  offlineStorage.init();
});

