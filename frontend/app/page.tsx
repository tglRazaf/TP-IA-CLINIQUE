"use client";

import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import {
  Sparkles,
  Languages,
  Brain,
  Mic,
  Search,
  CheckCircle,
} from "lucide-react";
import { motion } from "framer-motion";
import { useRouter } from "next/navigation";

export default function LandingPage() {
  const router = useRouter();
  return (
    <div className="min-h-screen bg-linear-to-b from-slate-950 to-slate-900 text-white">
      {/* HERO */}
      <section className="container mx-auto px-6 py-24 text-center">
        <motion.h1
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="text-4xl md:text-6xl font-extrabold leading-tight"
        >
          Éditeur de Texte Intelligent <br />
          <span className="text-indigo-400">pour la Langue Malagasy</span>
        </motion.h1>

        <p className="mt-6 text-lg text-slate-300 max-w-3xl mx-auto">
          Un outil innovant qui assiste les rédacteurs malgaches grâce à
          l’Intelligence Artificielle, même dans un contexte de langue à faibles
          ressources.
        </p>

        <div className="mt-10 flex justify-center gap-4">
          <Button
            onClick={() => router.push("/demo")}
            size="lg"
            className="rounded-2xl"
          >
            Essayer la Démo
          </Button>
          {/* <Button
            size="lg"
            variant="outline"
            className="text-black rounded-2xl"
          >
            Voir les Fonctionnalités
          </Button> */}
        </div>
      </section>

      {/* VALEUR */}
      <section className="container mx-auto px-6 py-20 grid md:grid-cols-3 gap-8">
        {[
          {
            icon: <Languages className="w-8 h-8 text-indigo-400" />,
            title: "Pensé pour le Malagasy",
            desc: "Contrairement aux éditeurs classiques, notre outil respecte les règles linguistiques et culturelles du Malagasy.",
          },
          {
            icon: <Brain className="w-8 h-8 text-indigo-400" />,
            title: "IA Hybride",
            desc: "Combinaison d’approches symboliques, algorithmiques et data-driven pour contourner le manque de données.",
          },
          {
            icon: <Sparkles className="w-8 h-8 text-indigo-400" />,
            title: "Productivité Augmentée",
            desc: "Écrivez plus vite, avec moins d’erreurs, tout en enrichissant votre vocabulaire.",
          },
        ].map((item, i) => (
          <Card
            key={i}
            className="bg-slate-800/60 border-slate-700 rounded-2xl"
          >
            <CardContent className="p-6 text-center">
              <div className="mb-4 flex justify-center">{item.icon}</div>
              <h3 className="text-xl font-semibold mb-2">{item.title}</h3>
              <p className="text-slate-300">{item.desc}</p>
            </CardContent>
          </Card>
        ))}
      </section>

      {/* FONCTIONNALITÉS */}
      <section className="bg-slate-900/60 py-24">
        <div className="container mx-auto px-6">
          <h2 className="text-3xl md:text-4xl font-bold text-center mb-16">
            Fonctionnalités Clés
          </h2>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            {[
              {
                icon: <CheckCircle />,
                title: "Correcteur Orthographique",
                desc: "Détection intelligente des fautes avec distance de Levenshtein et dictionnaires locaux.",
              },
              {
                icon: <Search />,
                title: "Explorateur Sémantique",
                desc: "Suggestions de concepts liés grâce à un graphe de connaissances malgache.",
              },
              {
                icon: <Brain />,
                title: "Autocomplétion",
                desc: "Prédiction du mot suivant via modèles N-grams entraînés sur des corpus locaux.",
              },
              {
                icon: <Languages />,
                title: "Traduction Mot-à-Mot",
                desc: "Cliquez sur un mot pour voir sa signification ou sa traduction instantanément.",
              },
              {
                icon: <Sparkles />,
                title: "Analyse de Sentiment",
                desc: "Identification simple des tonalités positives ou négatives du texte.",
              },
              {
                icon: <Mic />,
                title: "Synthèse Vocale",
                desc: "Écoutez votre texte lu avec un accent adapté au contexte local.",
              },
            ].map((f, i) => (
              <Card
                key={i}
                className="bg-slate-800/60 border-slate-700 rounded-2xl"
              >
                <CardContent className="p-6">
                  <div className="flex items-center gap-3 mb-3 text-indigo-400">
                    {f.icon}
                    <h3 className="text-lg font-semibold text-white">
                      {f.title}
                    </h3>
                  </div>
                  <p className="text-slate-300">{f.desc}</p>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="container mx-auto px-6 py-24 text-center">
        <h2 className="text-3xl md:text-4xl font-bold mb-6">
          Créez l’outil que Madagascar attend
        </h2>
        <p className="text-slate-300 max-w-2xl mx-auto mb-10">
          Ce projet académique démontre comment l’IA peut valoriser une langue à
          faibles ressources et soutenir la production écrite en Malagasy.
        </p>
        <Button
          onClick={() => router.push("/demo")}
          size="lg"
          className="rounded-2xl px-10"
        >
          Commencer Maintenant
        </Button>
      </section>

      {/* FOOTER */}
      <footer className="border-t border-slate-800 py-6 text-center text-slate-400 text-sm">
        Projet IA – Institut Supérieur Polytechnique de Madagascar
      </footer>
    </div>
  );
}
