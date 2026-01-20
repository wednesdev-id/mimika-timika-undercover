declare module 'react' {
  const React: any;
  export default React;
  export type ReactNode = any;
  export type FC<P = {}> = (props: P) => any;
}

declare module 'react/jsx-runtime' {
  export const jsx: any;
  export const jsxs: any;
  export const Fragment: any;
}

declare namespace JSX {
  interface IntrinsicElements {
    [elemName: string]: any;
  }
}