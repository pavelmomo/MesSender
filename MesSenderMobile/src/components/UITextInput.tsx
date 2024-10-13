import React from "react";
import {
  StyleProp,
  TextInput,
  TextStyle,
  StyleSheet,
  TextInputProps,
} from "react-native";

export default function UITextInput(props: TextInputProps) {
  return <TextInput {...props} style={[styles.main, props.style]}></TextInput>;
}

const styles = StyleSheet.create({
  main: { flex: 1 },
});
