import { NavigationContainer } from "@react-navigation/native";
import { observer } from "mobx-react-lite";
import { AuthRoutes, AppRoutes } from "./navigation";
import RootStore from "./store/RootStore";

const AppContainer = observer(() => {
  return (
    <NavigationContainer>
      {RootStore.authStore.isAuthorized ? <AppRoutes /> : <AuthRoutes />}
    </NavigationContainer>
  );
});

export default AppContainer;
