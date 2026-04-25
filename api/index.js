import ytdl from "ytdl-core";

export default async function handler(req, res) {
  const { url } = req.query;

  if (!url) {
    return res.status(400).json({ error: "URL missing" });
  }

  try {
    const info = await ytdl.getInfo(url);

    const formats = info.formats;

    const video = formats.find(f => f.hasVideo && f.hasAudio);
    const audio = formats.find(f => !f.hasVideo && f.hasAudio);

    res.status(200).json({
      title: info.videoDetails.title,
      video_url: video?.url,
      audio_url: audio?.url
    });

  } catch (e) {
    res.status(500).json({ error: e.message });
  }
}
