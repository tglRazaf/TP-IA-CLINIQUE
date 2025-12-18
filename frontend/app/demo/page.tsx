import EditorQuill from "@/components/editor/EditorQuill";
import { ArrowLeft } from "lucide-react";
import Link from "next/link";

export default function DemoPage() {
  return (
    <div className="min-h-screen bg-slate-950 text-white p-10">
      <h1 className="text-3xl font-bold mb-6">
        <span className=" flex gap-7 justify-center items-center">
          <Link href="/">
            <ArrowLeft className="w-9 h-9 cursor-pointer" />
          </Link>{" "}
          Éditeur Intelligent Malagasy
        </span>
      </h1>

      <EditorQuill />
    </div>
  );
}
