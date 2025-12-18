"use client";

import { useState } from "react";
import dynamic from "next/dynamic";
import "react-quill-new/dist/quill.snow.css";

const ReactQuill = dynamic(() => import("react-quill-new"), { ssr: false });

export default function EditorQuill() {
  const [value, setValue] = useState("");

  const modules = {
    toolbar: [
      [{ header: [1, 2, false] }],
      ["bold", "italic", "underline"],
      [{ list: "ordered" }, { list: "bullet" }],
      ["clean"],
    ],
  };

  const formats = ["header", "bold", "italic", "underline", "list"];

  return (
    <div className="bg-white text-black rounded-2xl shadow-xl">
      <ReactQuill
        theme="snow"
        value={value}
        onChange={setValue}
        modules={modules}
        formats={formats}
        placeholder="Soraty eto ny lahatsoratrao amin'ny teny malagasy…"
        className="min-h-[450px]"
      />
    </div>
  );
}
