from Settings import *
import pyray as rl

class TextureHandler:
    textures = {}  # Dictionary to hold all named textures

    def __init__(self) -> None:
        if not TextureHandler.textures:  # Load only once
            TextureHandler.bind()

    @classmethod
    def bind(cls):
        """Load or reload all textures into a dictionary."""

        def load_texture(name, path, wrap_repeat=False):
            texture = rl.load_texture(str(path))
            if wrap_repeat:
                rl.set_texture_wrap(texture, rl.TEXTURE_WRAP_REPEAT)
            cls.textures[name] = texture

        # Load named textures
        load_texture("player", imageDir / "player.png")
        load_texture("enemy", imageDir / "enemies" / "Skeleton.png")
        load_texture("background", imageDir / "infineDopplBackground.png")
        load_texture("rect_ui", imageDir / "rectUI.png")
        load_texture("enemy_arrow", imageDir / "enemies" / "skeletonArrow.png")
        load_texture("wooden_bow", imageDir / "woodenBow.png")
        load_texture("wooden_arrow", imageDir / "woodenArrow.png")
        load_texture("slime", imageDir / "enemies" / "slime.png")
        load_texture("skeleton_bow", imageDir / "enemies" / "skeletonBow.png")
        load_texture("bossTexture", imageDir / "finalBoss.png")
        load_texture("bossTexture2", imageDir / "finalBoss2.png")
        load_texture("boomerang", imageDir / "boomerang.png")
        load_texture("knightTex", imageDir / "enemies" / "knight.png")
        load_texture("swordArrow", imageDir / "enemies" / "throwableSword.png")
        load_texture("worldTiles", imageDir / "tiles" / "atlas.png")


        # Additional (repeatable) textures
        load_texture("flooring", imageDir / "flooring.png")
        load_texture("brickwall", imageDir / "brickwall2.png", wrap_repeat=True)
        load_texture("vomitBall", imageDir / "enemies" / "vomitBall.png")

    @classmethod
    def unbind(cls):
        """Unload all textures and clear the dictionary."""
        for texture in cls.textures.values():
            rl.unload_texture(texture)
        cls.textures.clear()

    @classmethod
    def get(cls, name):
        """Retrieve a texture by name."""
        return cls.textures.get(name)

    # Optional convenience methods
    @classmethod
    def getPlayerAtlas(cls):
        return cls.get("player")

    @classmethod
    def getEnemyAtlas(cls):
        return cls.get("enemy")

    @classmethod
    def getBackground(cls):
        return cls.get("background")

    @classmethod
    def getRectUI(cls):
        return cls.get("rect_ui")

    @classmethod
    def getArrow(cls):
        return cls.get("enemy_arrow")

    @classmethod
    def getWoodenArrow(cls):
        return cls.get("wooden_arrow")

    @classmethod
    def getWoodenBow(cls):
        return cls.get("wooden_bow")
    @classmethod
    def getTextureByIdx(cls, idx):
        names = ["player", "flooring", "brickwall"]
        return cls.get(names[idx])
        '''
        cls.textures.append(cls.atlasPlayer)
        cls.textures.append(rl.load_texture(str(imageDir / "flooring.png")))
        cls.textures.append(rl.load_texture(str(imageDir / "brickwall2.png")))
        '''



