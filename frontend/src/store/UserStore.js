import { makeAutoObservable } from "mobx";

class UserStore {
  user = null;

  constructor() {
    makeAutoObservable(this);
  }

  setOnClosed() {
    this.onceClose = true;
  }

  async setUser(user) {
    this.user = user;
    
  }

  clearUser() {
    this.user = null;
  }
}

const userStore = new UserStore();
export default userStore;