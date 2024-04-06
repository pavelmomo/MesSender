import React, { useState, useEffect } from "react";

export default function UsersTab() {
  return (
    <div
      style={{
        display: "flex",
        flexDirection: "row",
        alignItems: "flex-start",
        justifyContent: "center",
        flex: 10,
      }}
    >
      <div
        style={{
          marginTop: 5,
          height: "70%",
          border: "3px solid",
          borderColor: "var(--main-color)",
          borderRadius: "6px",
          boxShadow: "1px 1px 3px 0px #73513f",
        }}
      ></div>
    </div>
  );
}
