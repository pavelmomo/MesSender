import { makeAutoObservable } from "mobx";

export class AuthStore {
  isAuthorized: boolean = false;
  currentUser: UserDTO | null = null;
  constructor() {
    makeAutoObservable(this);
  }
  setAuthorized(param: boolean) {
    this.isAuthorized = param;
  }
  unauthorize() {
    this.isAuthorized = false;
    this.currentUser = null;
  }
}
