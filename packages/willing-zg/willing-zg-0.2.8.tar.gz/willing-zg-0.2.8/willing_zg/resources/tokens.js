import axios from 'axios';

const TOKEN_REFRESH_INTERVAL = 4 * 60 * 1000; // 4 min in ms

const PORTUNUS_URL = process.env.PORTUNUS_URL || 'https://dev.portunus.willing.com';

const defaultFetch = () =>
  axios({ method: 'post', url: `${PORTUNUS_URL}/api/auth/token/refresh/`, withCredentials: true });

const loginUrl = `${PORTUNUS_URL}/login`;

const defaultOnError = () => {
  const params = new URLSearchParams();
  params.append('next', window.location.href);
  window.location.replace(`${loginUrl}?${params.toString()}`);
};

class TokenFetcher {
  constructor() {
    this.fetchFunction = defaultFetch;
    this.onError = defaultOnError;
    this.onSuccess = () => null;
    this.accessToken = '';
    this.timerId = null;
  }

  fetchToken = async () => {
    try {
      const response = await this.fetchFunction();
      this.accessToken = response.data.access;
      this.onSuccess(this.accessToken);
      return true;
    } catch (error) {
      if (error.response) {
        if (error.response.status === 401) {
          this.clearToken();
        }
      }
      this.onError(error);
    }
    return false;
  };

  clearToken() {
    this.accessToken = '';
    clearInterval(this.timerId);
    this.timerId = null;
  }

  start(fetchFn, onSuccess, onError) {
    this.fetchFunction = fetchFn || this.fetchFunction;
    this.onSuccess = onSuccess || this.onSuccess;
    this.onError = onError || this.onError;
    if (!this.timerId) {
      this.timerId = setInterval(this.fetchToken, TOKEN_REFRESH_INTERVAL);
      this.fetchToken();
    }
  }
}

const tokenFetcher = new TokenFetcher();

export default tokenFetcher;
