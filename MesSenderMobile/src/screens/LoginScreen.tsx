import { observer } from "mobx-react-lite";
import {
  StyleSheet,
  View,
  TextInput,
  Button,
  Text,
  SafeAreaView,
} from "react-native";
import UITextInput from "../components/UITextInput";

const LoginScreen = observer(() => {
  return (
    <SafeAreaView style={styles.formContainer}>
      <View style={styles.formContainer}>
        <Text>Имя пользователя</Text>
        <UITextInput
          placeholder="Имя пользователя"
          style={{ flex: 0 }}
        ></UITextInput>
      </View>
    </SafeAreaView>
  );
});

const styles = StyleSheet.create({
  formContainer: {
    flex: 1,
  },
  rowContainer: {},
  bigBlue: {
    color: "blue",
    fontWeight: "bold",
    fontSize: 30,
  },
  red: {
    color: "red",
  },
});
export default LoginScreen;
