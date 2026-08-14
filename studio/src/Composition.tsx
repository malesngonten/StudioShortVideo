import { CalculateMetadataFunction, Composition, Audio, staticFile, Sequence, AbsoluteFill } from "remotion";
import { getAudioDurationInSeconds } from "@remotion/media-utils";
import scriptData from "./data/rencana_video.json";

type Scene = {
  urutan: number;
  teks: string;
  visual: string;
  mood: string;
};

type Props = {
  scenes: Scene[];
};

const moodColor: Record<string, string> = {
  misterius: "#1a1a2e",
  kaget: "#4a1a1a",
  santai: "#1a3a2e",
  dramatis: "#2e1a3a",
};

const calculateMetadata: CalculateMetadataFunction<Props> = async () => {
  const durationInSeconds = await getAudioDurationInSeconds(
    staticFile("audio/voiceover.mp3")
  );
  return {
    durationInFrames: Math.ceil(durationInSeconds * 30),
    props: { scenes: scriptData.scenes },
  };
};

export const MyComposition = () => {
  return (
    <Composition
      id="MyComp"
      component={MyComponent}
      durationInFrames={60}
      fps={30}
      width={1080}
      height={1920}
      calculateMetadata={calculateMetadata}
      defaultProps={{ scenes: [] }}
    />
  );
};

export const MyComponent: React.FC<Props> = ({ scenes }) => {
  const framesPerScene = scenes.length > 0 ? Math.floor(900 / scenes.length) : 900;

  return (
    <AbsoluteFill>
      <Audio src={staticFile("audio/voiceover.mp3")} />
      {scenes.map((scene, i) => (
        <Sequence key={scene.urutan} from={i * framesPerScene} durationInFrames={framesPerScene}>
          <AbsoluteFill
            style={{
              backgroundColor: moodColor[scene.mood] || "#1a1a2e",
              justifyContent: "center",
              alignItems: "center",
              padding: 60,
            }}
          >
            <div
              style={{
                color: "white",
                fontSize: 48,
                fontFamily: "sans-serif",
                textAlign: "center",
                fontWeight: "bold",
                textShadow: "0 2px 8px rgba(0,0,0,0.8)",
              }}
            >
              {scene.teks}
            </div>
          </AbsoluteFill>
        </Sequence>
      ))}
    </AbsoluteFill>
  );
};
