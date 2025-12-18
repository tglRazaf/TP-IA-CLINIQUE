import { useState } from "react";


export function SuggestionModal({ items, position, onSelect }: { items: string[], position: { x: number, y: number }, onSelect: (item: string) => void }) {
  return (
    <div
      style={{
        position: "fixed",
        top: position.y,
        left: position.x,
        background: "#fff",
        border: "1px solid #ddd",
        borderRadius: 6,
        boxShadow: "0 4px 12px rgba(0,0,0,.15)",
        minWidth: 200,
        zIndex: 1000
      }}
    >
      {items.map((item) => (
        <div
          key={item}
          onMouseDown={() => onSelect(item)}
          style={{
            padding: "8px 12px",
            cursor: "pointer"
          }}
        >
          {item}
        </div>
      ))}
    </div>
  );
}
