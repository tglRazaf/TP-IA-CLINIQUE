"use client";

import { useState } from "react";
import dynamic from "next/dynamic";
import "react-quill-new/dist/quill.snow.css";
import axios from "axios";
import { SuggestionModal } from "../ui/suggestion-modal";

const ReactQuill = dynamic(() => import("react-quill-new"), { ssr: false });

export default function EditorQuill() {
  const [value, setValue] = useState("");
  const [suggestions, setSuggestions] = useState([] as string[])
  const [correctedWords, setCorrectedWords] = useState([] as string[])
    const [show, setShow] = useState(false);
  const [pos, setPos] = useState({ x: 0, y: 0 });
  const [selectedWord, setSelectedWord] = useState({word: "", position: {x: 0, y: 0}});

  const modules = {
    toolbar: [
      [{ header: [1, 2, false] }],
      ["bold", "italic", "underline"],
      [{ list: "ordered" }, { list: "bullet" }],
      ["clean"],
    ],
  };

  function htmlToPlainText(html:string) {
    const div = document.createElement("div");
    div.innerHTML = html;
    return div.textContent || div.innerText || "";
  }

  const fetchNextWord = async () => {
    const words = value.length>1 ? value.trim().split(' ') : [value.trim()]
    setSuggestions([])
    try {
      const word = await axios.post('http://127.0.0.1:8000/api/predire-mot-suivant', {
        contexte: htmlToPlainText(value)
      })
      console.log(word.data['predictions'].length)
      for (let index = 0; index < word.data['predictions'].length; index++) {
        suggestions.push(`${htmlToPlainText(value)} ${word.data['predictions'][index]['mot']}`)
      }
      // setSuggestion(`${htmlToPlainText(value)} ${word.data['predictions'][0]['mot']}`)
    } catch (error) {
      console.log(error)
    }
    setSuggestions(suggestions)
  }

  const fetchCorrectWords = async (word: string) => {
    try {
      setCorrectedWords([])
      const words = await axios.post('http://127.0.0.1:8000/api/corriger', {
        texte: word
      })
      setCorrectedWords(words.data.data.suggestions)
    } catch (error) {
      console.log(error)
    }
  }

  const onKeyUp = (event: KeyboardEvent) => {
    fetchNextWord()
  }

  const formats = ["header", "bold", "italic", "underline", "list"];

  const handleSuggestionClick = (suggestion: string) => {
    setValue(suggestion)
    setSuggestions([])
  }

  const onRightClick = (event: React.MouseEvent) => {
    event.preventDefault();
    // alert(correctedWords.join(', '))
    setShow(true)
    setPos({ x: event.clientX, y: event.clientY })
  }

  const handleSelectionChange = (range: any) => {
    const pleinText = htmlToPlainText(value)
    try {
      setSelectedWord({
        word: pleinText.split('').slice(range.index, range.index + range.length).join(''),
        position: { x: range.index, y: range.index + range.length }
      })
      fetchCorrectWords(pleinText.split('').slice(range.index, range.index + range.length).join(''))
    } catch (error) {
      console.log("No word selected");
    }
  };

  const handleCorrection = (word: string) => {
    const plainText = htmlToPlainText(value)
    const correctedText =
    plainText.slice(0, selectedWord.position.x) +
    word +
    plainText.slice(selectedWord.position.y);

  setValue(correctedText);
    setShow(false)
  }

  const customSetValue = (value: string) => {
    setValue(value)
if(value == ''){
      setSuggestions([])
      return
    }
  }

  return (
    <div className="text-black rounded-2xl shadow-xl" onContextMenu={onRightClick}>
      <ReactQuill
        onChangeSelection={handleSelectionChange}
        theme="snow"
        value={value}
        onChange={setValue}
        modules={modules}
        formats={formats}
        placeholder="Soraty eto ny lahatsoratrao amin'ny teny malagasy…"
        className="min-h-[250px] bg-white border-none"
        onKeyUp={onKeyUp}
      />
      <div className="suggested-words text-white mt-2">
        <p className="w-screen">{suggestions.map((suggestion, index) => (
          <span className="cursor-pointer py-1 my-2 hover:bg-gray-400" key={index} onClick={()=> handleSuggestionClick(suggestion)}>{suggestion}<br/></span>
        ))}</p>
      </div>
      {show && (
        <SuggestionModal
          items={correctedWords}
          position={pos}
          onSelect={(item) => {
            handleCorrection(item);
            setShow(false);
          }}
        />
      )}
    </div>
  );
}
