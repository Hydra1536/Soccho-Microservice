// Global app logic
class SocchoApp {
  constructor() {
    this.initOfflineSupport();
    this.initHTMX();
  }

  initOfflineSupport() {
    window.addEventListener('online', () => {
      document.body.classList.remove('offline');
      // Sync queued transactions
      this.syncOfflineTransactions();
    });

    window.addEventListener('offline', () => {
      document.body.classList.add('offline');
      // Show offline banner
      this.showOfflineBanner();
    });
  }

  initHTMX() {
    document.body.addEventListener('htmx:responseError', (e) => {
      // Show error toast
      this.showToast('Network error. Please try again.', 'error');
    });
  }

  syncOfflineTransactions() {
    // IndexedDB sync logic
    console.log('Syncing offline transactions...');
  }

  showOfflineBanner() {
    // Create/show offline banner
  }

  showToast(message, type = 'info') {
    // Toast notification
  }
}

// Init app
document.addEventListener('DOMContentLoaded', () => {
  new SocchoApp();
});

