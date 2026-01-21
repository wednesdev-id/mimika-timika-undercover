import React from "react";

type Props = React.ButtonHTMLAttributes<HTMLButtonElement> & {
  variant?: "primary" | "secondary";
};

export function Button({ variant = "primary", ...props }: Props) {
  const base = {
    padding: "8px 12px",
    borderRadius: "6px",
    border: "none",
    cursor: "pointer",
    fontWeight: 600,
  } as const;
  const styles =
    variant === "primary"
      ? {
          backgroundColor: "var(--color-primary-500)",
          color: "white",
        }
      : {
          backgroundColor: "var(--color-surface)",
          color: "var(--color-text-primary)",
          border: "1px solid var(--color-primary-400)",
        };

  return <button style={{ ...base, ...styles }} {...props} />;
}
