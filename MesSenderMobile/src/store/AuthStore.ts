import { makeAutoObservable, runInAction } from "mobx";
import AsyncStorage from "@react-native-async-storage/async-storage";
import { getCurrentUser } from "../api/user";
import { TOKEN_STORAGE_KEY } from "../constant/app";

export class AuthStore {
  isAuthorized: boolean = false;
  currentUser: UserDTO | null = null;

  constructor() {
    makeAutoObservable(this);
  }

  async unauthorize() {
    await AsyncStorage.removeItem(TOKEN_STORAGE_KEY);
    runInAction(() => {
      this.isAuthorized = false;
      this.currentUser = null;
    });
  }

  setCurrentUser(user: UserDTO) {
    this.currentUser = user;
    this.isAuthorized = true;
  }

  async getCurrentUser() {
    const savedToken = await AsyncStorage.getItem(TOKEN_STORAGE_KEY);
    if (!savedToken) {
      return;
    }
    const user = await getCurrentUser(savedToken);
    if (user != null) {
      this.setCurrentUser(user);
    }
  }
}
