import { AuthStore } from "./AuthStore";

class RootStore {
  authStore: AuthStore;
  constructor() {
    this.authStore = new AuthStore();
  }
}

export default new RootStore();
