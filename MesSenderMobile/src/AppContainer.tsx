import { useEffect } from "react";
import { NavigationContainer } from "@react-navigation/native";
import { observer } from "mobx-react-lite";
import { AuthRoutes, AppRoutes } from "./navigation/navigation";
import RootStore from "./store/RootStore";

const AppContainer = observer(() => {
  console.log("main component rendered!!!");
  useEffect(() => {
    RootStore.authStore.getCurrentUser();
  }, []);
  return (
    <NavigationContainer>
      {RootStore.authStore.isAuthorized ? <AppRoutes /> : <AuthRoutes />}
    </NavigationContainer>
  );
});

export default AppContainer;
